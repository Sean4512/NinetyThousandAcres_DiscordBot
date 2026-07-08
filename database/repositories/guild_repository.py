# -*- coding: utf-8 -*-
"""
@File    : guild_repository.py
@Time    : 2026/4/14 下午 09:51
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from database.repositories.core import BaseRepository

from utils.sql_loader import load_sql


class GuildProfileRepository(BaseRepository):
    _sql_insert_guild_profiles = load_sql("sert", "insert_guild_profiles.sql")
    _sql_exists_by_id = load_sql("queries", "exists_guild_profile_by_guild_id.sql")

    @classmethod
    def insert_guild_profile(
        cls,
        guild_id: str,
        created_at: str,
    ):
        cls.run_sql_execute(cls._sql_insert_guild_profiles, (guild_id, created_at))

    @classmethod
    def is_exists(
        cls,
        guild_id: str,
    ) -> bool:
        cursor = cls.run_sql_execute(cls._sql_exists_by_id, (guild_id,))
        row = cursor.fetchone()
        return bool(row[0]) if row is not None else False


class GuildConfigRepository(BaseRepository):
    _sql_upsert_guild_config = load_sql("sert", "upsert_guild_config.sql")
    _sql_get_by_id = load_sql("queries", "get_guild_config_by_id.sql")

    @classmethod
    def upsert_guild_config(
        cls,
        guild_id: str,
        configs: dict[str, str],
        created_at: str,
        updated_at: str,
    ):
        for key, value in configs.items():
            cls.run_sql_execute(
                cls._sql_upsert_guild_config,
                (
                    guild_id,
                    key,
                    value,
                    created_at,
                    updated_at,
                )
            )

    @classmethod
    def get_config_by_id(
        cls,
        *,
        guild_id: str,
    ) -> dict[str, str]:
        cursor = cls.run_sql_execute(cls._sql_get_by_id, (guild_id,))
        rows = cursor.fetchall()
        guild_configs = {
            row["field_key"]: (row["config_value"] if row["config_value"] is not None else "") for row in rows
        }
        return guild_configs

