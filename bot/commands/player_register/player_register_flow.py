# -*- coding: utf-8 -*-
"""
@File    : player_register_flow.py
@Time    : 2026/6/16 下午 04:33
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations

import discord

from bot.commands.questionnaire import QuestionnaireFlow
from services.player_profiles_service import PlayerRegistrationService
from utils.Types.questionnaire import (
    Questionnaire,
    QuestionnaireResult,
)
from utils.exceptions.discord_exceptions import InternalError


class PlayerRegisterFlow(QuestionnaireFlow):
    def __init__(
        self,
        *,
        user: discord.User | discord.Member,
        guild_id: str,
        discord_id: str,
        questionnaire: Questionnaire,
        timeout_seconds: int,
        is_update: bool = False,
        initial_answers: dict | None = None,
    ) -> None:
        self.guild_id = guild_id
        self.discord_id = discord_id
        self.is_update = is_update

        super().__init__(
            user=user,
            questionnaire=questionnaire,
            timeout_seconds=timeout_seconds,
            initial_answers=initial_answers,
            start_button_label=(
                "開始更新資料"
                if is_update
                else "開始註冊"
            ),
            completed_message=(
                "🎉 玩家資料更新完成。"
                if is_update
                else "🎉 玩家註冊完成。"
            ),
        )

    async def on_completed(
        self,
        *,
        interaction: discord.Interaction,
        result: QuestionnaireResult,
    ) -> None:
        success, message = (
            PlayerRegistrationService.register_player(
                discord_id=self.discord_id,
                guild_id=self.guild_id,
                answers=result.answers,
                fields=self.questionnaire.fields,
                is_update=self.is_update,
            )
        )

        if not success:
            raise InternalError(message)

        self.logger.info(
            "Player questionnaire completed. "
            "operator_id=%s, player_id=%s, "
            "guild_id=%s, is_update=%s",
            interaction.user.id,
            self.discord_id,
            self.guild_id,
            self.is_update,
        )