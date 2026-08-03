# -*- coding: utf-8 -*-
"""
@File    : __init__.py
@Time    : 2026/8/1 下午 09:23
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from discord.ext import commands

from utils.logger import get_discord_bot_logger

from .creation import MatchSignupCreationCog
from .registration import MatchSignupRegistrationCog

async def setup(bot: commands.Bot):
    discord_bot_logger = get_discord_bot_logger()
    discord_bot_logger.debug("loading MatchSignupRegistration Cog...")
    await bot.add_cog(MatchSignupRegistrationCog(bot))



