# -*- coding: utf-8 -*-
"""
@File    : MatchSignup.py.py
@Time    : 2026/4/28 下午 03:45
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.core import BaseCog, BaseView
from bot.commands.admin_test import admin_required
from utils.logger import get_discord_bot_logger


class MatchSignupCog(BaseCog):

    @app_commands.command(
        name="create_match_signup",
        description="在當前頻道建立一個永久的報名面板",
    )
    @app_commands.guild_only()
    @admin_required()
    async def create_match_signup(
        self,
        interaction: discord.Interaction
    ) -> None:

        await self.send_interaction_message(interaction, "321")




async def setup(bot: commands.Bot):
    discord_bot_logger = get_discord_bot_logger()
    discord_bot_logger.debug("loading Match Signup Cog...")
    await bot.add_cog(MatchSignupCog(bot))



