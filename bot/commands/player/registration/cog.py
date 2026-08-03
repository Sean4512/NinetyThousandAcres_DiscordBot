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

from services.player import PlayerRegistrationService

from utils.exceptions.discord_exceptions import GuildRequiredError
from utils.exceptions.service_exceptions import PlayerAlreadyRegisteredError, PlayerNotRegisteredError

class PlayerRegistrationCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.runner = DiscordQuestionnaireRunner()


    @app_commands.command(name="player_registration", description="玩家註冊", )
    @app_commands.guild_only()
    async def registration(self, interaction: discord.Interaction):

        guild = interaction.guild
        if guild is None:
            raise GuildRequiredError()

        user = interaction.user

        if PlayerRegistrationService.is_registered(guild.id, user.id):
            raise PlayerAlreadyRegisteredError()

        questionnaire = get_player_register_questionnaire()
        result = await self.runner.run(questionnaire, interaction)

        if not result.completed:
            return

        PlayerRegistrationService.register(guild.id, user.id, questionnaire, result.answers)

    @app_commands.command(name="player_registration_update", description="玩家更新資料", )
    @app_commands.guild_only()
    async def update(self, interaction: discord.Interaction):

        guild = interaction.guild
        if guild is None:
            raise GuildRequiredError()

        user = interaction.user
        if not PlayerRegistrationService.is_registered(guild.id, user.id):
            raise PlayerNotRegisteredError()

        answers = PlayerRegistrationService.get_answers_map(guild.id, user.id)

        questionnaire = get_player_register_questionnaire()
        result = await self.runner.run(questionnaire, interaction, initial_answers=answers)

        if not result.completed:
            return

        PlayerRegistrationService.update_answers(guild.id, user.id, questionnaire, result.answers)

    @app_commands.command(name="player_registration_delete", description="玩家刪除資料", )
    @app_commands.guild_only()
    async def unregister(self, interaction: discord.Interaction):
        guild = interaction.guild
        if guild is None:
            raise GuildRequiredError()

        user = interaction.user
        if not PlayerRegistrationService.is_registered(guild.id, user.id):
            raise PlayerNotRegisteredError()

        PlayerRegistrationService.unregister(guild.id, user.id)

        await self.safe_reply(interaction, f"✅ {user.global_name} 玩家資料已刪除")


