# -*- coding: utf-8 -*-
"""
@File    : base_cog.py
@Time    : 2026/7/1 下午 01:00
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.core.utils import InteractionResponderMixin

from utils.logger import get_discord_bot_logger

__all__ = ["BaseCog"]


class BaseCog(commands.Cog, InteractionResponderMixin):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = get_discord_bot_logger()

    async def cog_app_command_error(
            self,
            interaction: discord.Interaction,
            error: app_commands.AppCommandError,
    ) -> None:
        await self.handle_app_error(interaction, error)


