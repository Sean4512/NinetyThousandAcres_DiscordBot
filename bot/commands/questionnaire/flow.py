# -*- coding: utf-8 -*-
"""
@File    : flow.py
@Time    : 2026/6/16 下午 04:02
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

import discord

from bot.core.utils import InteractionResponderMixin
from utils.Types.questionnaire import Questionnaire, QuestionnaireResult, QuestionnaireDestination
from utils.exceptions.discord_exceptions import InternalError
from utils.logger import get_discord_bot_logger

if TYPE_CHECKING:
    from .view import QuestionnaireStepView


class QuestionnaireFlow(ABC, InteractionResponderMixin):
    """
    通用私訊問答流程控制器。

    負責：
    1. 傳送問答開始訊息
    2. 控制目前步驟
    3. 保存使用者答案
    4. 開啟指定步驟 Modal
    5. 完成後產生 QuestionnaireResult
    6. 呼叫各功能自行實作的 on_completed()
    """

    def __init__(
        self,
        *,
        user: discord.User | discord.Member,
        questionnaire: Questionnaire,
        timeout_seconds: int,
        initial_answers: dict[str, Any] | None = None,
        start_button_label: str = "開始填寫",
        next_button_label: str = "下一步",
        cancel_button_label: str = "取消",
        completed_message: str = "🎉 表單填寫完成，資料已送出。",
        cancelled_message: str = "🚫 問答流程已取消。",
    ) -> None:
        self.user = user
        self.questionnaire = questionnaire
        self.timeout_seconds = timeout_seconds

        self.start_button_label = start_button_label
        self.next_button_label = next_button_label
        self.cancel_button_label = cancel_button_label

        self.completed_message = completed_message
        self.cancelled_message = cancelled_message

        self.answers: dict[str, Any] = dict(initial_answers or {})

        self.active_views: list[QuestionnaireStepView] = []

        self.is_completed = False
        self.is_cancelled = False

        self.logger = get_discord_bot_logger()

    @property
    def is_ended(self) -> bool:
        """
        問答流程是否已經結束。

        包含：
        - 正常完成
        - 使用者取消
        """
        return self.is_completed or self.is_cancelled

    async def cancel(
            self,
            *,
            interaction: discord.Interaction,
            source_message: discord.Message | None,
    ) -> None:
        """
        取消問答流程。

        負責：
        1. 標記流程已取消
        2. 停止全部 View
        3. 清除目前訊息的按鈕
        4. 呼叫子類別取消 hook
        5. 回覆取消訊息
        """
        if self.is_ended:
            await self.send_interaction_message(
                interaction=interaction,
                message="此問答流程已經結束。",
                ephemeral=True,
            )
            return

        self.is_cancelled = True

        for view in self.active_views:
            view.finish_view()

        message_edited = False

        if source_message is not None:
            try:
                await source_message.edit(
                    content=self.cancelled_message,
                    embed=None,
                    view=None,
                )
                message_edited = True

            except discord.NotFound:
                pass

            except discord.Forbidden:
                pass

            except discord.HTTPException:
                self.logger.exception(
                    "Failed to edit cancelled questionnaire message. "
                    "user_id=%s",
                    self.user.id,
                )

        try:
            await self.on_cancelled(
                interaction=interaction,
                answers=self.answers.copy(),
            )

        except Exception:
            self.logger.exception(
                "Questionnaire on_cancelled hook failed. "
                "user_id=%s",
                self.user.id,
            )

        # if not interaction.response.is_done():
        #     await interaction.response.defer()

        if not interaction.response.is_done():
            if message_edited:
                await interaction.response.defer()
            else:
                await interaction.response.send_message(
                    self.cancelled_message,
                    ephemeral=self.questionnaire.delivery.interaction_ephemeral,
                )

    async def on_cancelled(
            self,
            *,
            interaction: discord.Interaction,
            answers: dict[str, Any],
    ) -> None:
        """
        問答取消後的額外處理。

        子類別可以選擇覆寫，例如：
        - 記錄取消 log
        - 刪除暫存資料
        - 更新報名狀態
        - 通知管理員

        預設不做任何處理。
        """
        return

    @property
    def allowed_user_id(self) -> int:
        """
        允許操作這份問卷的 Discord 使用者 ID。
        """
        return self.user.id

    async def start(self, *, interaction: discord.Interaction,) -> discord.Message:
        """
        啟動問答流程。
        """
        if not self.questionnaire.steps:
            raise InternalError("問答流程尚未設定任何步驟。")

        embed = self.build_start_embed()

        # return await self.send_step_button_message(
        #     step_index=0,
        #     button_label=self.start_button_label,
        #     embed=embed,
        # )

        return await self.send_step_button_message(
            interaction=interaction,
            step_index=0,
            button_label=self.start_button_label,
            embed=embed,
        )

    async def open_step_modal(
            self,
            *,
            interaction: discord.Interaction,
            step_index: int,
            source_message: discord.Message | None,
    ) -> None:
        from bot.commands.questionnaire.modal import QuestionnaireStepModal

        if self.is_ended:
            message = (
                "此問答流程已取消。"
                if self.is_cancelled
                else "此問答流程已經完成。"
            )

            await self.send_interaction_message(
                interaction=interaction,
                message=message,
                ephemeral=True,
            )
            return

        if step_index < 0 or step_index >= len(self.questionnaire.steps):
            raise InternalError(
                f"問答步驟不存在。step_index={step_index}"
            )

        modal = QuestionnaireStepModal(
            flow=self,
            step_index=step_index,
            source_message=source_message,
        )

        await interaction.response.send_modal(modal)

    async def advance_after_step_completed(
        self,
        *,
        interaction: discord.Interaction,
        step_index: int,
        source_message: discord.Message | None,
    ) -> None:
        """
        使用者完成目前步驟後，進入下一步或完成流程。
        """
        await self.disable_step_message(
            source_message=source_message,
            step_index=step_index,
        )

        next_step_index = step_index + 1

        if next_step_index >= len(self.questionnaire.steps):
            await self.finish(interaction=interaction)
            return

        await self.send_step_button_message(
            interaction=interaction,
            step_index=next_step_index,
            button_label=self.next_button_label,
        )

    async def finish(
            self,
            *,
            interaction: discord.Interaction,
    ) -> None:
        if self.is_ended:
            return

        self.is_completed = True

        result = QuestionnaireResult(
            answers=self.answers.copy(),
            completed=True,
        )

        try:
            await self.on_completed(
                interaction=interaction,
                result=result,
            )

        except Exception:
            self.logger.exception(
                "Questionnaire on_completed hook failed. user_id=%s",
                self.user.id,
            )
            raise

        for view in self.active_views:
            view.finish_view()

        # await self.send_interaction_message(
        #     interaction=interaction,
        #     message=self.completed_message,
        #     ephemeral=False,
        # )
        await self.send_questionnaire_message(
            interaction=interaction,
            content=self.completed_message,
        )

    @abstractmethod
    async def on_completed(
        self,
        *,
        interaction: discord.Interaction,
        result: QuestionnaireResult,
    ) -> None:
        """
        問答完成後的業務邏輯。

        子類別必須自行實作，例如：
        - 儲存玩家資料
        - 儲存比賽報名資料
        - 發送管理員審核訊息
        - 寫入其他資料表
        """
        raise NotImplementedError

    async def send_step_button_message(
        self,
        *,
        interaction: discord.Interaction,
        step_index: int,
        button_label: str,
        embed: discord.Embed | None = None,
    ) -> discord.Message:
        """
        傳送指定步驟的按鈕訊息。
        """
        from .view import QuestionnaireStepView

        view = QuestionnaireStepView(
            flow=self,
            step_index=step_index,
            button_label=button_label,
            timeout=self.timeout_seconds,
        )

        # message = await self.user.send(
        #     embed=embed,
        #     view=view,
        # )
        message = await self.send_questionnaire_message(
            interaction=interaction,
            embed=embed,
            view=view,
        )

        view.set_message(message)
        self.active_views.append(view)

        return message

    async def disable_step_message(
        self,
        *,
        source_message: discord.Message | None,
        step_index: int,
    ) -> None:
        """
        移除已完成步驟的按鈕，避免重複操作。
        """
        if source_message is None:
            return

        try:
            await source_message.edit(
                content=f"✅ 第 {step_index + 1} 步已完成。",
                embed=None,
                view=None,
            )

        except discord.NotFound:
            pass

        except discord.Forbidden:
            pass

        except discord.HTTPException:
            self.logger.exception(
                "Failed to disable questionnaire step message. "
                "user_id=%s, step_index=%s",
                self.user.id,
                step_index,
            )

    def build_start_embed(self) -> discord.Embed:
        """
        建立問答流程開始訊息。
        """
        description_parts: list[str] = []

        if self.questionnaire.description:
            description_parts.append(self.questionnaire.description)

        description_parts.extend(
            [
                f"本表單共 {len(self.questionnaire.steps)} 個步驟。",
                (
                    f"每個步驟有效時間為 "
                    f"{self.timeout_seconds // 60} 分鐘。"
                ),
            ]
        )

        return discord.Embed(
            title=self.questionnaire.title,
            description="\n\n".join(description_parts),
            color=discord.Color.green(),
        )

    async def send_questionnaire_message(
            self,
            *,
            interaction: discord.Interaction,
            content: str | None = None,
            embed: discord.Embed | None = None,
            view: discord.ui.View | None = None,
    ) -> discord.Message:
        """
        根據 QuestionnaireDelivery 發送問卷訊息。

        DIRECT_MESSAGE:
            使用 user.send()

        CHANNEL / THREAD:
            使用 interaction.response 或 interaction.followup

        EPHEMERAL:
            只有操作使用者可見

        PUBLIC:
            頻道內所有成員可見
        """
        delivery = self.questionnaire.delivery

        if delivery.is_direct_message:
            return await self.user.send(
                content=content,
                embed=embed,
                view=view,
            )

        self.validate_interaction_destination(interaction)

        ephemeral = delivery.is_ephemeral

        if interaction.response.is_done():
            message = await interaction.followup.send(
                content=content,
                embed=embed,
                view=view,
                ephemeral=ephemeral,
                wait=True,
            )
            return message

        await interaction.response.send_message(
            content=content,
            embed=embed,
            view=view,
            ephemeral=ephemeral,
        )

        return await interaction.original_response()

    def validate_interaction_destination(
            self,
            interaction: discord.Interaction,
    ) -> None:
        """
        驗證 Interaction 發生位置是否符合 QuestionnaireDelivery。
        """
        destination = self.questionnaire.delivery.destination
        channel = interaction.channel

        if destination is QuestionnaireDestination.DIRECT_MESSAGE:
            return

        if interaction.guild is None:
            raise InternalError("此問卷必須在伺服器中執行。")

        if destination is QuestionnaireDestination.THREAD:
            if not isinstance(channel, discord.Thread):
                raise InternalError("此問卷只能在討論串中執行。")
            return

        if destination is QuestionnaireDestination.CHANNEL:
            if isinstance(channel, discord.Thread):
                raise InternalError("此問卷不能在討論串中執行。")

            if not isinstance(
                    channel,
                    (
                            discord.TextChannel,
                            discord.VoiceChannel,
                            discord.StageChannel,
                    ),
            ):
                raise InternalError("此問卷必須在伺服器頻道中執行。")
