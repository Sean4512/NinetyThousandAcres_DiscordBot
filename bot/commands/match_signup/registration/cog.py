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
from bot.commands.match_signup.helpers import get_registration_forum, ensure_thread_in_forum
from config.questionnaire_settings import get_match_signup_questionnaire
from services.guild_service import GuildService, GuildConfigKeys
from services.match_signup.form_service import MatchSignupConfigKeys, MatchSignupFormService, MatchSignupThreadStatus
from utils.exceptions.discord_exceptions import GuildRequiredError, GuildNotInitializedError
from utils.exceptions.service_exceptions import MatchSignupFormNotFoundError


class MatchSignupGroup(app_commands.Group):
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
        self.questionnaire_runner = DiscordQuestionnaireRunner()

    match_signup = MatchSignupGroup(
        name="match_signup",
        description="戰役報名相關指令",
        guild_only=True,
    )

    @match_signup.command(name="register", description="報名戰役")
    async def register(self, interaction: discord.Interaction, ):

        guild: discord.Guild = interaction.guild
        thread = interaction.channel

        registration_forum_id = GuildService.get_config_value(guild.id, GuildConfigKeys.REGISTRATION_FORUM_ID,)
        if registration_forum_id is None:
            raise GuildNotInitializedError()

        registration_forum = await get_registration_forum(guild, registration_forum_id, )
        if registration_forum is None:
            raise GuildNotInitializedError()

        ensure_thread_in_forum(guild, registration_forum, thread)

        if not MatchSignupFormService.exists(guild.id, thread.id):
            raise MatchSignupFormNotFoundError()



        questionnaire = get_match_signup_questionnaire()
        result = await self.questionnaire_runner.run(questionnaire, interaction)




