# -*- coding: utf-8 -*-
"""
@File    : modal.py
@Time    : 2026/8/2 下午 10:21
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 問卷單一步驟的 Discord Modal。
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

import discord

from bot.core import BaseModal
from bot.core.utils import ensure_owner

from utils.models.questionnaire import QuestionComponentType, QuestionField
from utils.questionnaire_field import validate_questionnaire_field

if TYPE_CHECKING:
    from bot.core.questionnaire.runner import _QuestionnaireSession

__all__ = ["QuestionnaireStepModal"]


class QuestionnaireStepModal(BaseModal):
    """把問卷某一步的欄位組成 Discord Modal，並在提交時驗證、寫回 session。"""

    def __init__(
        self,
        *,
        session: _QuestionnaireSession,
        step_index: int,
        source_message: discord.Message | None,
    ) -> None:
        self.session = session
        self.step_index = step_index
        self.source_message = source_message
        self.step = session.questionnaire.steps[step_index]

        # Discord Modal title 最多 45 字元。
        modal_title = f"{session.questionnaire.title} - 第 {step_index + 1} 步"
        super().__init__(title=modal_title[:45])

        self.inputs: dict[str, discord.ui.TextInput] = {}
        for question_field in self.step.fields:
            text_input = discord.ui.TextInput(
                label=question_field.label[:45],
                placeholder=question_field.placeholder or None,
                required=question_field.required,
                min_length=question_field.min_length,
                max_length=question_field.max_length,
                style=self._get_text_input_style(question_field),
                default=self._get_default_value(question_field.key),
            )
            self.inputs[question_field.key] = text_input
            self.add_item(text_input)

    def _get_default_value(self, field_key: str) -> str | None:
        """把 session 內既有的答案轉成 TextInput 可用的字串。"""
        value = self.session.answers.get(field_key)
        if value is None:
            return None
        if isinstance(value, bool):
            return "是" if value else "否"
        return str(value)

    @staticmethod
    def _get_text_input_style(question_field: QuestionField) -> discord.TextStyle:
        if question_field.component_type == QuestionComponentType.TEXT:
            return discord.TextStyle.short
        if question_field.component_type == QuestionComponentType.PARAGRAPH:
            return discord.TextStyle.paragraph
        raise ValueError(f"Modal 不支援此欄位類型：{question_field.component_type}")

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if not await ensure_owner(interaction, self.session.allowed_user_id):
            await self.safe_reply(interaction, "這不是你的問答流程。", ephemeral=True)
            return

        if self.session.is_ended:
            message = (
                "此問答流程已取消。"
                if self.session.is_cancelled
                else "此問答流程已經完成。"
            )
            await self.safe_reply(interaction, message, ephemeral=True)
            return

        step_answers: dict[str, Any] = {}
        for question_field in self.step.fields:
            text_input = self.inputs[question_field.key]
            is_valid, normalized_value, error_message = validate_questionnaire_field(
                field=question_field,
                raw_value=text_input.value,
            )

            if not is_valid:
                await self.safe_reply(
                    interaction,
                    f"❌ {error_message}\n\n請重新點擊按鈕填寫第 {self.step_index + 1} 步。",
                    ephemeral=True,
                )
                return

            step_answers[question_field.key] = normalized_value

        # 全部欄位驗證成功後，才一次寫回答案。
        self.session.answers.update(step_answers)

        # 先 defer，避免後續發訊息 / 存資料超過 Discord 的 3 秒限制。
        if not interaction.response.is_done():
            await interaction.response.defer()

        await self.session.advance_after_step_completed(
            interaction,
            step_index=self.step_index,
            source_message=self.source_message,
        )
