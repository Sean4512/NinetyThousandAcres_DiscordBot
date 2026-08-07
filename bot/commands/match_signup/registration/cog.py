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
from services.guild_service import GuildService
from utils.exceptions.discord_exceptions import GuildRequiredError, GuildNotInitializedError


class MatchSignupRegistrationGroup(app_commands.Group):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:

        guild = interaction.guild
        if guild is None:
            raise GuildRequiredError()

        if not GuildService.is_initialized(interaction.guild.id):
            raise GuildNotInitializedError()

        return True

class MatchSignupRegistrationCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.runner = DiscordQuestionnaireRunner()




