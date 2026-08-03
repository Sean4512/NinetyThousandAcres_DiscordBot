# -*- coding: utf-8 -*-
"""
@File    : runner.py
@Time    : 2026/8/2 下午 10:21
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : Discord 介面的問卷執行器。
"""

from __future__ import annotations

import asyncio
from typing import Any

import discord

from bot.core.senders import dispatch_message
from bot.core.utils import InteractionResponderMixin

from utils.questionnaire_runner import QuestionnaireRunner
from utils.models.questionnaire import Questionnaire, QuestionnaireResult
from utils.exceptions.discord_exceptions import InternalError
from utils.logger import get_discord_bot_logger

__all__ = ["DiscordQuestionnaireRunner"]


class DiscordQuestionnaireRunner(QuestionnaireRunner[discord.Interaction]):
    """用 Discord（多步驟按鈕 + Modal）呈現問卷、收集答案。

    本身「無狀態」：每次 run() 都會建立一個 _QuestionnaireSession 來裝那一次
    作答的狀態，因此同一個 runner 實例可以安全地被多人同時使用。

    答完要做什麼（存資料、審核…）不在這裡處理——run() 只把 QuestionnaireResult
    回傳給呼叫端，由呼叫端（cog / service）決定。
    """

    def __init__(
        self,
        *,
        timeout_seconds: int = 300,
        start_button_label: str = "開始填寫",
        next_button_label: str = "下一步",
        cancel_button_label: str = "取消",
        completed_message: str = "🎉 表單填寫完成，資料已送出。",
        cancelled_message: str = "🚫 問答流程已取消。",
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.start_button_label = start_button_label
        self.next_button_label = next_button_label
        self.cancel_button_label = cancel_button_label
        self.completed_message = completed_message
        self.cancelled_message = cancelled_message
        self.logger = get_discord_bot_logger()

    async def run(
        self,
        questionnaire: Questionnaire,
        context: discord.Interaction,
        *,
        initial_answers: dict[str, Any] | None = None,
    ) -> QuestionnaireResult:
        if not questionnaire.steps:
            raise InternalError("問答流程尚未設定任何步驟。")

        session = _QuestionnaireSession(
            runner=self,
            questionnaire=questionnaire,
            interaction=context,
            initial_answers=initial_answers,
        )

        # 送出第一步的按鈕訊息，然後卡在 Future 上，直到最後一步完成或使用者取消。
        await session.start(context)
        return await session.wait_result()


class _QuestionnaireSession(InteractionResponderMixin):
    """單次問卷作答的狀態機（僅供 DiscordQuestionnaireRunner 內部使用）。

    負責：控制目前步驟、暫存答案、開 Modal、逐步推進、完成/取消時把結果
    塞進 Future。modal / view 都回呼到這個 session 上。
    """

    def __init__(
        self,
        *,
        runner: DiscordQuestionnaireRunner,
        questionnaire: Questionnaire,
        interaction: discord.Interaction,
        initial_answers: dict[str, Any] | None = None,
    ) -> None:
        self.runner = runner
        self.questionnaire = questionnaire
        self.user: discord.User | discord.Member = interaction.user

        # 複製一份，避免直接改到呼叫端傳進來的 dict。
        self.answers: dict[str, Any] = dict(initial_answers or {})

        self.active_views: list[discord.ui.View] = []

        self.is_completed = False
        self.is_cancelled = False

        self.logger = get_discord_bot_logger()
        self._future: asyncio.Future[QuestionnaireResult] = (
            asyncio.get_running_loop().create_future()
        )

    # ------------------------------------------------------------------ #
    # 對外：run() 用來等結果
    # ------------------------------------------------------------------ #
    async def wait_result(self) -> QuestionnaireResult:
        return await self._future

    def _resolve(self, result: QuestionnaireResult) -> None:
        if not self._future.done():
            self._future.set_result(result)

    @property
    def allowed_user_id(self) -> int:
        return self.user.id

    @property
    def is_ended(self) -> bool:
        return self.is_completed or self.is_cancelled

    # ------------------------------------------------------------------ #
    # 流程控制
    # ------------------------------------------------------------------ #
    async def start(self, interaction: discord.Interaction) -> None:
        delivery = self.questionnaire.delivery

        # 問卷走私訊時，觸發的 interaction（例如群組斜線指令）不會被後續流程碰到，
        # 必須自己在 3 秒內簽收，否則 Discord 會顯示「該申請未受回應」。
        # 用 defer() 只簽收、不宣稱任何事，內容與結果稍後用 followup 回報。
        if delivery.is_direct_message and not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

        embed = self._build_start_embed()
        # 若私訊送不出去（使用者關閉私訊），user.send() 會丟 discord.Forbidden，
        # 這裡不攔截，交給 cog 的 handle_app_error 統一回覆「無法私訊你」，
        # 就不會誤報「已私訊給你」，也避免重複處理。
        await self._send_step_button_message(
            interaction,
            step_index=0,
            button_label=self.runner.start_button_label,
            embed=embed,
        )

        # 私訊確認送達後，才在使用者「輸入指令的地方」回報。
        if delivery.is_direct_message:
            await interaction.followup.send(
                "📩 已將表單私訊給你，請查看你的私訊。",
                ephemeral=True,
            )

    async def open_step_modal(
        self,
        interaction: discord.Interaction,
        *,
        step_index: int,
        source_message: discord.Message | None,
    ) -> None:
        from bot.core.questionnaire.modal import QuestionnaireStepModal

        if self.is_ended:
            await self._reply_already_ended(interaction)
            return

        if step_index < 0 or step_index >= len(self.questionnaire.steps):
            raise InternalError(f"問答步驟不存在。step_index={step_index}")

        modal = QuestionnaireStepModal(
            session=self,
            step_index=step_index,
            source_message=source_message,
        )
        await interaction.response.send_modal(modal)

    async def advance_after_step_completed(
        self,
        interaction: discord.Interaction,
        *,
        step_index: int,
        source_message: discord.Message | None,
    ) -> None:
        await self._disable_step_message(source_message, step_index)

        next_step_index = step_index + 1
        if next_step_index >= len(self.questionnaire.steps):
            await self._finish(interaction)
            return

        await self._send_step_button_message(
            interaction,
            step_index=next_step_index,
            button_label=self.runner.next_button_label,
        )

    async def cancel(
        self,
        interaction: discord.Interaction,
        *,
        source_message: discord.Message | None,
    ) -> None:
        if self.is_ended:
            await self._reply_already_ended(interaction)
            return

        self.is_cancelled = True
        self._stop_views()

        message_edited = await self._edit_message_safe(
            source_message,
            content=self.runner.cancelled_message,
        )

        if not interaction.response.is_done():
            if message_edited:
                await interaction.response.defer()
            else:
                await interaction.response.send_message(
                    self.runner.cancelled_message,
                    ephemeral=self.questionnaire.delivery.interaction_ephemeral,
                )

        self._resolve(
            QuestionnaireResult(answers=self.answers.copy(), completed=False)
        )

    async def _finish(self, interaction: discord.Interaction) -> None:
        if self.is_ended:
            return

        self.is_completed = True
        self._stop_views()

        await dispatch_message(
            interaction,
            self.questionnaire.delivery,
            user=self.user,
            content=self.runner.completed_message,
        )

        self._resolve(
            QuestionnaireResult(answers=self.answers.copy(), completed=True)
        )

    # ------------------------------------------------------------------ #
    # 訊息 / UI 輔助
    # ------------------------------------------------------------------ #
    async def _send_step_button_message(
        self,
        interaction: discord.Interaction,
        *,
        step_index: int,
        button_label: str,
        embed: discord.Embed | None = None,
    ) -> discord.Message:
        from bot.core.questionnaire.view import QuestionnaireStepView

        view = QuestionnaireStepView(
            session=self,
            step_index=step_index,
            button_label=button_label,
            timeout=self.runner.timeout_seconds,
        )

        message = await dispatch_message(
            interaction,
            self.questionnaire.delivery,
            user=self.user,
            embed=embed,
            view=view,
        )

        view.set_message(message)
        self.active_views.append(view)
        return message

    async def _disable_step_message(
        self,
        source_message: discord.Message | None,
        step_index: int,
    ) -> None:
        await self._edit_message_safe(
            source_message,
            content=f"✅ 第 {step_index + 1} 步已完成。",
        )

    async def _edit_message_safe(
        self,
        message: discord.Message | None,
        *,
        content: str,
    ) -> bool:
        """編輯訊息並清掉 embed/view；回傳是否有成功編輯。"""
        if message is None:
            return False
        try:
            await message.edit(content=content, embed=None, view=None)
            return True
        except discord.NotFound:
            return False
        except discord.Forbidden:
            return False
        except discord.HTTPException:
            self.logger.exception(
                "Failed to edit questionnaire message. user_id=%s",
                self.user.id,
            )
            return False

    def _stop_views(self) -> None:
        for view in self.active_views:
            view.stop()

    def _build_start_embed(self) -> discord.Embed:
        description_parts: list[str] = []
        if self.questionnaire.description:
            description_parts.append(self.questionnaire.description)

        description_parts.extend(
            [
                f"本表單共 {len(self.questionnaire.steps)} 個步驟。",
                f"每個步驟有效時間為 {self.runner.timeout_seconds // 60} 分鐘。",
            ]
        )

        return discord.Embed(
            title=self.questionnaire.title,
            description="\n\n".join(description_parts),
            color=discord.Color.green(),
        )

    async def _reply_already_ended(self, interaction: discord.Interaction) -> None:
        message = "此問答流程已取消。" if self.is_cancelled else "此問答流程已經完成。"
        await self.safe_reply(interaction, message, ephemeral=True)
