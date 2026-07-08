# -*- coding: utf-8 -*-
"""
@File    : ping.py.py
@Time    : 2026/4/11 上午 02:59
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord import app_commands
from discord.ext import commands
from bot.core.base_cog import BaseCog

from utils.logger import get_discord_bot_logger


class PingCog(BaseCog):

    @app_commands.command(name="ping", description="測試 bot 是否正常運作")
    async def ping(self, interaction: discord.Interaction):
        message = "Pong! Bot Test successful。"
        await self.send_interaction_message(interaction, message)


async def setup(bot: commands.Bot):
    discord_bot_logger = get_discord_bot_logger()
    discord_bot_logger.debug("loading Ping Cog...")
    await bot.add_cog(PingCog(bot))