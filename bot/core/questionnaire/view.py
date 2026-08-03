# -*- coding: utf-8 -*-
"""
@File    : view.py
@Time    : 2026/8/2 下午 10:21
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 問卷每一步的按鈕 View（開啟 Modal / 取消）。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from bot.core import BaseView

if TYPE_CHECKING:
    from bot.core.questionnaire.runner import _QuestionnaireSession

__all__ = ["QuestionnaireStepView"]


class QuestionnaireStepView(BaseView):
    """一顆「開始/下一步」按鈕 + 一顆「取消」按鈕，回呼到 session。"""

    def __init__(
        self,
        *,
        session: _QuestionnaireSession,
        step_index: int,
        button_label: str,
        timeout: float | None,
    ) -> None:
        super().__init__(
            allowed_user_id=session.allowed_user_id,
            timeout_message="⏰ 此問答步驟已超過有效時間，請重新操作。",
            timeout=timeout,
        )

        self.session = session
        self.step_index = step_index

        self.open_modal_button.label = button_label
        self.cancel_button.label = session.runner.cancel_button_label

        if step_index == 0:
            self.open_modal_button.style = discord.ButtonStyle.success
        else:
            self.open_modal_button.style = discord.ButtonStyle.primary

    @discord.ui.button(label="開始填寫", style=discord.ButtonStyle.success, row=0)
    async def open_modal_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        await self.session.open_step_modal(
            interaction,
            step_index=self.step_index,
            source_message=interaction.message,
        )

    @discord.ui.button(label="取消", style=discord.ButtonStyle.danger, row=0)
    async def cancel_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        await self.session.cancel(
            interaction,
            source_message=interaction.message,
        )
