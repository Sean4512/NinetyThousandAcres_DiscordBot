# -*- coding: utf-8 -*-
"""
@File    : base_view.py
@Time    : 2026/5/7 下午 05:02
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord import app_commands

from bot.core.utils import InteractionResponderMixin
from utils.logger import get_discord_bot_logger
from utils.exceptions import DISCORD_EXCEPTIONS, InternalError


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

        if interaction.user.id != self.allowed_user_id:
            await self.send_interaction_message(
                interaction=interaction,
                message="這不是你的操作流程。",
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
        original_error = getattr(error, "original", error)

        if isinstance(original_error, DISCORD_EXCEPTIONS):
            await self.send_interaction_message(
                interaction,
                str(original_error),
            )
            return

        if isinstance(original_error, discord.Forbidden):
            await self.send_interaction_message(
                interaction,
                "❌ 無法私訊你，請確認你有開啟伺服器成員私訊。"
            )
            return

        if isinstance(original_error, app_commands.NoPrivateMessage):
            await self.send_interaction_message(
                interaction,
                "這個指令只能在伺服器中使用。",
            )
            self.logger.warning(
                f"User {interaction.user.name}({interaction.user.id}) is executing the /setup, but guild is None")
            return

        if isinstance(error, app_commands.CheckFailure):
            await self.send_interaction_message(
                interaction,
                "你沒有權限使用這個指令。",
            )
            return

        self.logger.exception(
            "Unhandled app command error. command=%s, user_id=%s",
            interaction.command.qualified_name if interaction.command else "unknown_command",
            interaction.user.id,
            exc_info=error,
        )
        await self.send_interaction_message(
            interaction,
            InternalError().message,
        )
