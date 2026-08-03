# -*- coding: utf-8 -*-
"""
@File    : admin_cog.py
@Time    : 2026/8/3 下午 10:05
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 管理員 建立/更新/刪除 玩家註冊資料
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.core import BaseCog, DiscordQuestionnaireRunner
from bot.core.permissions import ensure_admin_interaction
from config.questionnaire_settings import get_player_register_questionnaire

from services.player import PlayerRegistrationService

from utils.logger import get_discord_bot_logger
from utils.exceptions.discord_exceptions import GuildRequiredError
from utils.exceptions.service_exceptions import (
    PlayerAlreadyRegisteredError,
    PlayerNotRegisteredError,
)


class PlayerAdminGroup(app_commands.Group):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return await ensure_admin_interaction(interaction)

class PlayerRegistrationAdminCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.runner = DiscordQuestionnaireRunner()

    player_admin = PlayerAdminGroup(
        name="player_admin",
        description="管理員 管理玩家註冊資料",
        guild_only=True,
    )

    @player_admin.command(name="register", description="幫指定玩家建立註冊資料")
    async def register(self, interaction: discord.Interaction, member: discord.Member,):

        guild = interaction.guild
        if guild is None:
            raise GuildRequiredError()

        if PlayerRegistrationService.is_registered(guild.id, member.id):
            raise PlayerAlreadyRegisteredError()

        questionnaire = get_player_register_questionnaire()
        result = await self.runner.run(questionnaire, interaction)

        if not result.completed:
            return

        PlayerRegistrationService.register(
            guild.id, member.id, questionnaire, result.answers,
        )

    @player_admin.command(name="update", description="更新指定玩家的註冊資料")
    async def update(self, interaction: discord.Interaction, member: discord.Member):

        guild = interaction.guild
        if guild is None:
            raise GuildRequiredError()

        if not PlayerRegistrationService.is_registered(guild.id, member.id):
            raise PlayerNotRegisteredError()

        answers = PlayerRegistrationService.get_answers_map(guild.id, member.id)

        questionnaire = get_player_register_questionnaire()
        result = await self.runner.run(questionnaire, interaction, initial_answers=answers)

        if not result.completed:
            return

        PlayerRegistrationService.update_answers(guild.id, member.id, questionnaire, result.answers)


    @player_admin.command(name="delete", description="刪除指定玩家的註冊資料")
    async def delete(self, interaction: discord.Interaction, member: discord.Member):

        guild = interaction.guild
        if guild is None:
            raise GuildRequiredError()

        if not PlayerRegistrationService.is_registered(guild.id, member.id):
            raise PlayerNotRegisteredError()

        PlayerRegistrationService.unregister(guild.id, member.id)

        await self.safe_reply(interaction, f"✅ {member.mention} 玩家資料已刪除")


