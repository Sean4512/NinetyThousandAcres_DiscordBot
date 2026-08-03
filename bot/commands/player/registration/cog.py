# -*- coding: utf-8 -*-
"""
@File    : cog.py
@Time    : 2026/8/3 上午 02:19
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord import app_commands

from bot.core import BaseCog, DiscordQuestionnaireRunner
from config.questionnaire_settings import get_player_register_questionnaire


class PlayerRegistrationCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.runner = DiscordQuestionnaireRunner()


    @app_commands.command(name="player_registration", description="玩家註冊", )
    @app_commands.guild_only()
    async def signup(self, interaction: discord.Interaction):
        questionnaire = get_player_register_questionnaire()
        result = await self.runner.run(questionnaire, interaction)
        self.logger.info(result)





