# -*- coding: utf-8 -*-
"""
@File    : base_modal.py
@Time    : 2026/5/8 下午 01:57
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord import app_commands

from utils.logger import get_discord_bot_logger
from utils.exceptions import DISCORD_EXCEPTIONS, InternalError
from bot.core.utils import InteractionResponderMixin

__all__ = ["BaseModal"]


class BaseModal(discord.ui.Modal, InteractionResponderMixin):

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.logger = get_discord_bot_logger()


    default_error_message = "伺服器內部出現異常，請稍後再試或聯繫 Bot 開發者。"

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: Exception,
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
