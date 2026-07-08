# -*- coding: utf-8 -*-
"""
@File    : match_signup_cog.py
@Time    : 2026/6/16 下午 06:23
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations

import discord
from discord import app_commands

from config.settings import get_discord_bot_settings
from config.questionnaire_settings import get_match_signup_questionnaire, get_create_match_signup_questionnaire

from bot.core import BaseCog, BaseView
from bot.commands.admin_test import admin_required

from services import GuildService, MatchSignupService

from utils.exceptions.discord_exceptions import (
    DebugError,
    GuildNotInitializedError, InternalError, GuildOnlyError, PlayerNoRegisteredError, ParameterError
)

from .match_signup_flow import CreateMatchSignupFlow, PlayerMatchSignupView


# class MatchSignupRegisterButton(BaseView):
#
#     def __init__(self):





class MatchSignupCog(BaseCog):

    async def cog_load(self) -> None:

        self.bot.add_view(
            PlayerMatchSignupView()
        )


    async def start_create_match_signup(
        self,
        interaction: discord.Interaction,
        match_signup_config,
    ):

        raise DebugError()




    @app_commands.command(
        name="create_match_signup_forms",
        description="在當前頻道建立一個永久的報名面板",
    )
    @app_commands.guild_only()
    @admin_required()
    async def create_match_signup_forms(
        self,
        interaction: discord.Interaction
    ) -> None:
        guild = interaction.guild
        if guild is None:
            raise GuildOnlyError()

        user = interaction.user
        guild_id = str(guild.id)
        discord_id = str(user.id)

        guild_config = GuildService.get_config_by_id(guild_id=guild_id)
        if guild_config is None:
            raise GuildNotInitializedError()

        registration_forum_id = guild_config.get("registration_forum_id", None)
        if registration_forum_id is None:
            raise GuildNotInitializedError()

        forum = await MatchSignupService.get_registration_forum(
            guild,
            registration_forum_id,
        )
        if forum is None:
            raise GuildNotInitializedError()

        is_update = False

        try:
            discord_bot_settings = get_discord_bot_settings()

            questionnaire = get_create_match_signup_questionnaire()
            initial_answers = {}

            flow = CreateMatchSignupFlow(
                user=user,
                guild=guild,
                discord_id=discord_id,
                questionnaire=questionnaire,
                timeout_seconds=(
                    discord_bot_settings.PLAYER_REGISTER_TIMEOUT
                ),
                is_update=is_update,
                initial_answers=initial_answers,
            )

            await flow.start(interaction=interaction)

        except Exception:
            raise

        if questionnaire.delivery.is_direct_message:
            await self.send_interaction_message(
                interaction=interaction,
                message="✅ 申請表單 已透過私訊傳送給你，請前往私訊查看。"
            )
        else:
            await self.send_interaction_message(
                interaction=interaction,
                message="✅ 申請表單 已傳送給你。"
            )
