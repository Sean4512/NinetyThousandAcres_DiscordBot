# -*- coding: utf-8 -*-
"""
@File    : modal.py
@Time    : 2026/6/16 下午 04:07
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

import discord

from bot.core import BaseModal
from bot.core.utils import ensure_allowed_user
from utils.Types.questionnaire import (
    QuestionComponentType,
    QuestionField,
)
from utils.questionnaire_field import validate_questionnaire_field

if TYPE_CHECKING:
    from .flow import QuestionnaireFlow


class QuestionnaireStepModal(BaseModal):
    """
    通用問答流程的單一步驟 Modal。
    """

    def __init__(
        self,
        *,
        flow: QuestionnaireFlow,
        step_index: int,
        source_message: discord.Message | None,
    ) -> None:
        self.flow = flow
        self.step_index = step_index
        self.source_message = source_message

        self.step = flow.questionnaire.steps[step_index]

        modal_title = (
            f"{flow.questionnaire.title} - "
            f"第 {step_index + 1} 步"
        )

        # Discord Modal title 最多 45 個字元。
        super().__init__(
            title=modal_title[:45],
        )

        self.inputs: dict[str, discord.ui.TextInput] = {}

        for question_field in self.step.fields:
            text_input = discord.ui.TextInput(
                label=question_field.label[:45],
                placeholder=question_field.placeholder or None,
                required=question_field.required,
                min_length=question_field.min_length,
                max_length=question_field.max_length,
                style=self.get_text_input_style(question_field),
                default=self.get_default_value(question_field.key),
            )

            self.inputs[question_field.key] = text_input
            self.add_item(text_input)

    def get_default_value(
        self,
        field_key: str,
    ) -> str | None:
        """
        將既有答案轉成 Discord TextInput 可以使用的字串。
        """
        value = self.flow.answers.get(field_key)

        if value is None:
            return None

        if isinstance(value, bool):
            return "是" if value else "否"

        return str(value)

    @staticmethod
    def get_text_input_style(
        question_field: QuestionField,
    ) -> discord.TextStyle:
        """
        取得欄位對應的 Discord TextInput Style。
        """
        if (
            question_field.component_type
            == QuestionComponentType.TEXT
        ):
            return discord.TextStyle.short

        if (
            question_field.component_type
            == QuestionComponentType.PARAGRAPH
        ):
            return discord.TextStyle.paragraph

        raise ValueError(
            "Modal 不支援此欄位類型："
            f"{question_field.component_type}"
        )

    async def on_submit(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """
        使用者提交目前步驟時觸發。
        """
        if not await ensure_allowed_user(
            interaction=interaction,
            allowed_user_id=self.flow.allowed_user_id,
            message="這不是你的問答流程。",
        ):
            return

        if self.flow.is_ended:
            message = (
                "此問答流程已取消。"
                if self.flow.is_cancelled
                else "此問答流程已經完成。"
            )

            await self.send_interaction_message(
                interaction=interaction,
                message=message,
                ephemeral=True,
            )
            return

        step_answers: dict[str, Any] = {}

        for question_field in self.step.fields:
            text_input = self.inputs[question_field.key]

            (
                is_valid,
                normalized_value,
                error_message,
            ) = validate_questionnaire_field(
                field=question_field,
                raw_value=text_input.value,
            )

            if not is_valid:
                await self.send_interaction_message(
                    interaction=interaction,
                    message=(
                        f"❌ {error_message}\n\n"
                        f"請重新點擊按鈕填寫"
                        f"第 {self.step_index + 1} 步。"
                    ),
                    ephemeral=True,
                )
                return

            step_answers[question_field.key] = normalized_value

        # 所有欄位都驗證成功後，才一次更新答案。
        self.flow.answers.update(step_answers)

        # 先回應 Discord，避免後續傳送訊息或資料庫操作超過 3 秒。
        if not interaction.response.is_done():
            await interaction.response.defer()

        await self.flow.advance_after_step_completed(
            interaction=interaction,
            step_index=self.step_index,
            source_message=self.source_message,
        )