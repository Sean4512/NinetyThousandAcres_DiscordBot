# -*- coding: utf-8 -*-
"""
@File    : base_modal.py
@Time    : 2026/7/1 下午 04:26
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord

from bot.core.utils import InteractionResponderMixin

from utils.logger import get_discord_bot_logger

__all__ = ["BaseModal"]


class BaseModal(discord.ui.Modal, InteractionResponderMixin):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_discord_bot_logger()

    async def on_error(
            self,
            interaction: discord.Interaction,
            error: Exception,
    ) -> None:
        await self.handle_app_error(interaction, error)
