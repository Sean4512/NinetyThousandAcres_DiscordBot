# -*- coding: utf-8 -*-
"""
@File    : player_profiles_service.py
@Time    : 2026/5/7 下午 11:55
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from datetime import datetime, timezone

from database.repositories.player_profiles_repository import PlayerProfilesRepository, PlayerProfileAnswersRepository
from utils.Types.database_types import PlayerProfiles

from utils.Types.questionnaire import *


class PlayerProfilesService:

    @staticmethod
    def insert_player_profile(
        discord_id: str,
        guild_id: str,
        admin_notes: str = "",
    ) -> tuple[bool, str]:

        now = datetime.now(timezone.utc).isoformat()
        player_profiles = PlayerProfilesService.get_player_profiles_by_id(guild_id, discord_id)

        checks = [
            ("discord_id", discord_id, str, "discord_id 不是字串"),
            ("guild_id", guild_id, str, "guild_id 不是字串"),
            ("admin_notes", admin_notes, str, "admin_notes 不是字串"),
        ]
        for field_name, value, expected_type, error_message in checks:
            if not isinstance(value, expected_type):
                return False, error_message

        if player_profiles is None:
            PlayerProfilesRepository.insert_player_profile(
                discord_id = discord_id,
                guild_id=guild_id,
                admin_notes=admin_notes,
                created_at=now,
                updated_at=now,
            )

        else:
            message = "你在此伺服器已經註冊過了, 若想修改請使用別的指令"
            return True, message

        return True, "此伺服器已完成初始化。"


    @staticmethod
    def get_player_profiles_by_id(guild_id: str, discord_id: str) -> PlayerProfiles | None:
        return PlayerProfilesRepository.get_by_id(guild_id, discord_id)

    @staticmethod
    def upsert_answers(
        *,
        guild_id: str,
        discord_id: str,
        answers: dict[str, str],
        field_labels: dict[str, str],
        is_update: bool = False
    ) -> tuple[bool, str]:

        now = datetime.now(timezone.utc).isoformat()
        player_profiles = PlayerProfilesService.get_player_profiles_by_id(guild_id, discord_id)

        if player_profiles is not None:
            if is_update:
                answers = { k:v for k, v in answers.items() if v }
            PlayerProfileAnswersRepository.upsert_answers(
                guild_id=guild_id,
                discord_id=discord_id,
                answers=answers,
                field_labels=field_labels,
                created_at=now,
                updated_at=now,
            )

        else:
            message = "尚未在此伺服器註冊過"
            return False, message

        return True, "資料更新完成。"

    @staticmethod
    def delete_by_id(guild_id: str, discord_id: str) -> None:
        PlayerProfilesRepository.delete_by_id(guild_id=guild_id,discord_id=discord_id)

    @staticmethod
    def get_player_profile_answers(guild_id: str, discord_id: str) -> dict[str, str]:
        return PlayerProfileAnswersRepository.get_answers_by_id(
            guild_id=guild_id,
            discord_id=discord_id,
        )

class PlayerRegistrationService:

    @classmethod
    def register_player(
        cls,
        *,
        guild_id: str,
        discord_id: str,
        answers: dict[str, str],
        fields: list[QuestionField],
        is_update: bool = False
    ) -> tuple[bool, str]:

        field_labels = {
            field.key: field.label
            for field in fields
        }

        success, message = PlayerProfilesService.insert_player_profile(
            discord_id=discord_id,
            guild_id=guild_id
        )

        if not success:
            return success, message

        success, message = PlayerProfilesService.upsert_answers(
            discord_id=discord_id,
            guild_id=guild_id,
            answers=answers,
            field_labels=field_labels,
            is_update=is_update
        )

        return success, message


