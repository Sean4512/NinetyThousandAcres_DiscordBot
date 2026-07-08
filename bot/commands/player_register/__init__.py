# -*- coding: utf-8 -*-
"""
@File    : __init__.py
@Time    : 2026/6/16 下午 04:33
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from discord.ext import commands

from utils.logger import get_discord_bot_logger

from .player_register_cog import PlayerRegisterCog

async def setup(bot: commands.Bot) -> None:
    logger = get_discord_bot_logger()
    logger.debug("loading PlayerRegisterCog...")
    await bot.add_cog(PlayerRegisterCog(bot))


