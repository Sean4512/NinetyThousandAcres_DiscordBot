# -*- coding: utf-8 -*-
"""
@File    : base_view.py
@Time    : 2026/7/1 下午 04:29
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord import app_commands

from bot.core.utils import InteractionResponderMixin, ensure_owner
from utils.exceptions.discord_exceptions import FlowOwnerMismatchError
from utils.logger import get_discord_bot_logger

__all__ = ["BaseView"]


class BaseView(discord.ui.View, InteractionResponderMixin):

    def __init__(
        self,
        *,
        allowed_user_id: int | None = None,
        timeout_message: str = "⏰ 此步驟已超過有效時間，請重新操作。",
        # timeout: float | None = 300,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.allowed_user_id = allowed_user_id
        self.timeout_message = timeout_message
        self.message: discord.Message | None = None
        self.logger = get_discord_bot_logger()

    def set_message(self, message: discord.Message | None):
        self.message = message

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.allowed_user_id is None:
            return True

        # if interaction.user.id != self.allowed_user_id:
        if not await ensure_owner(interaction, self.allowed_user_id):
            await self.safe_reply(
                interaction=interaction,
                message=FlowOwnerMismatchError().message,
            )
            return False

        return True

    async def on_timeout(self) -> None:
        if self.message is None:
            return

        try:
            await self.message.edit(
                content=self.timeout_message,
                view=None,
            )
        except discord.HTTPException:
            pass

    def finish_view(self) -> None:
        self.stop()

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
        item: discord.ui.Item,
    ) -> None:
        await self.handle_app_error(interaction, error)

