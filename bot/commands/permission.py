# -*- coding: utf-8 -*-
"""
@File    : permission.py
@Time    : 2026/7/25 上午 02:02
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.core import BaseCog, is_guild_admin

from utils.logger import get_discord_bot_logger
from utils.exceptions.discord_exceptions import GuildRequiredError


class PermissionCog(BaseCog):

    @app_commands.command(name="check-admin", description="檢查你是否具有本伺服器的管理員身分組")
    @app_commands.guild_only()
    @is_guild_admin()
    async def check_admin(self, interaction: discord.Interaction,):

        guild = interaction.guild
        if guild is None:
            raise GuildRequiredError()

        await self.safe_reply(interaction, f"你有對應的身分組權限。")


async def setup(bot: commands.Bot):
    discord_bot_logger = get_discord_bot_logger()
    discord_bot_logger.debug("loading Permission Cog...")
    await bot.add_cog(PermissionCog(bot))

