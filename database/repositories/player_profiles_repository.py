# -*- coding: utf-8 -*-
"""
@File    : player_profiles_repository.py
@Time    : 2026/5/8 上午 01:14
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""


from database.repositories.core import BaseRepository

from utils.sql_loader import load_sql
from utils.Types.database_types import PlayerProfiles


class PlayerProfilesRepository(BaseRepository):
    _sql_get_by_id = load_sql("queries", "get_player_profiles_by_id.sql")
    _sql_insert_player_profiles = load_sql("sert", "insert_player_profile.sql")
    _sql_delete_player_profiles_by_id = load_sql("delete", "delete_player_profiles_by_id.sql")

    @classmethod
    def insert_player_profile(
        cls,
        discord_id: str,
        guild_id: str,
        admin_notes: str | None,
        created_at: str,
        updated_at: str,
    ) -> None:
        cls.run_sql_execute(
            cls._sql_insert_player_profiles,
            (
                discord_id,
                guild_id,
                admin_notes,
                created_at,
                updated_at,
            )
        )

    @classmethod
    def get_by_id(cls, guild_id: str, discord_id: str, ) -> PlayerProfiles | None:
        cursor = cls.run_sql_execute(
            cls._sql_get_by_id,
            (
                guild_id,
                discord_id
            )
        )
        row = cursor.fetchone()
        if row is None:
            return None

        return PlayerProfiles(
            discord_id=row["discord_id"],
            guild_id=row["guild_id"],
            admin_notes=row["admin_notes"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @classmethod
    def delete_by_id(cls, guild_id: str, discord_id: str) -> None:
        cls.run_sql_execute(
            cls._sql_delete_player_profiles_by_id,
            (
                discord_id,
                guild_id,
            )
        )


class PlayerProfileAnswersRepository(BaseRepository):
    _sql_insert_player_profile_answers_repository = load_sql("sert", "insert_player_profile_answers_repository.sql")
    _sql_get_player_profile_answers_by_id = load_sql(
        "queries",
        "get_player_profile_answers_by_id.sql",
    )

    @classmethod
    def upsert_answers(
        cls,
        *,
        guild_id: str,
        discord_id: str,
        answers: dict[str, str],
        field_labels: dict[str, str],
        created_at: str,
        updated_at: str,
    ) -> None:
        for field_key, answer in answers.items():
            cls.run_sql_execute(
                cls._sql_insert_player_profile_answers_repository,
                (
                    guild_id,
                    discord_id,
                    field_key,
                    field_labels.get(field_key, field_key),
                    answer,
                    created_at,
                    updated_at,
                )
            )

    @classmethod
    def get_answers_by_id(
        cls,
        *,
        discord_id: str,
        guild_id: str,
    ) -> dict[str, str]:
        cursor = cls.run_sql_execute(
            cls._sql_get_player_profile_answers_by_id,
            (
                discord_id,
                guild_id,
            )
        )
        rows = cursor.fetchall()
        answers = {row["field_key"]: (row["answer"] if row["answer"] is not None else "") for row in rows}

        return answers

