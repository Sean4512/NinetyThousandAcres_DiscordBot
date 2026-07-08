# -*- coding: utf-8 -*-
"""
@File    : view.py
@Time    : 2026/6/16 下午 04:06
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from bot.core import BaseView

if TYPE_CHECKING:
    from .flow import QuestionnaireFlow


class QuestionnaireStepView(BaseView):
    def __init__(
        self,
        *,
        flow: QuestionnaireFlow,
        step_index: int,
        button_label: str,
        timeout: float | None,
    ) -> None:
        super().__init__(
            allowed_user_id=flow.allowed_user_id,
            timeout=timeout,
            timeout_message="⏰ 此問答步驟已超過有效時間，請重新操作。",
        )

        self.flow = flow
        self.step_index = step_index

        self.open_modal_button.label = button_label
        self.cancel_button.label = flow.cancel_button_label

        if step_index == 0:
            self.open_modal_button.style = discord.ButtonStyle.success
        else:
            self.open_modal_button.style = discord.ButtonStyle.primary

    @discord.ui.button(
        label="開始填寫",
        style=discord.ButtonStyle.success,
        row=0,
    )
    async def open_modal_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        await self.flow.open_step_modal(
            interaction=interaction,
            step_index=self.step_index,
            source_message=interaction.message,
        )

    @discord.ui.button(
        label="取消",
        style=discord.ButtonStyle.danger,
        row=0,
    )
    async def cancel_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        await self.flow.cancel(
            interaction=interaction,
            source_message=interaction.message,
        )
