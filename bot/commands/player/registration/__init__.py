# -*- coding: utf-8 -*-
"""
@File    : __init__.py
@Time    : 2026/8/3 上午 02:19
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from discord.ext import commands

from utils.logger import get_discord_bot_logger

from .cog import PlayerRegistrationCog

async def setup(bot: commands.Bot):
    discord_bot_logger = get_discord_bot_logger()
    discord_bot_logger.debug("loading PlayerRegistration Cog...")
    await bot.add_cog(PlayerRegistrationCog(bot))
