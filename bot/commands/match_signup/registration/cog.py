# -*- coding: utf-8 -*-
"""
@File    : cog.py
@Time    : 2026/8/1 下午 09:28
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord import app_commands

from bot.core import BaseCog, DiscordQuestionnaireRunner
from config.questionnaire_settings import get_match_signup_questionnaire


class MatchSignupRegistrationCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.runner = DiscordQuestionnaireRunner()


    @app_commands.command(name="match_signup", description="戰爭報名", )
    @app_commands.guild_only()
    async def signup(self, interaction: discord.Interaction):
        questionnaire = get_match_signup_questionnaire()
        result = await self.runner.run(questionnaire, interaction)
        self.logger.info(result)

