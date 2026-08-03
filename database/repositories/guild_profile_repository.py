# -*- coding: utf-8 -*-
"""
@File    : guild_profile_repository.py
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : guild_profiles 與 guild_configs 的資料庫操作
"""

import sqlite3

from database.core import BaseRepository
from database.repositories._base import load_cached_sql


class GuildProfileRepository:

    # ---------- guild_profiles ----------

    @staticmethod
    def insert_profile(guild_id: str, submitted_at: str) -> int:
        """新增 guild_profiles（已存在會拋 IntegrityError）。回傳受影響列數。"""
        sql = load_cached_sql("writes", "guild_profiles_insert.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "submitted_at": submitted_at,
        })

    @staticmethod
    def get_profile(guild_id: str) -> sqlite3.Row | None:
        """讀取單一 guild_profiles（submitted_at）。"""
        sql = load_cached_sql("reads", "guild_profiles_get.sql")
        return BaseRepository.run_sql_fetchone(sql, {"guild_id": guild_id})

    @staticmethod
    def exists_profile(guild_id: str) -> bool:
        """檢查 guild_profiles 是否存在。"""
        sql = load_cached_sql("reads", "guild_profiles_exists.sql")
        row = BaseRepository.run_sql_fetchone(sql, {"guild_id": guild_id})
        return bool(row["is_exists"]) if row else False

    @staticmethod
    def delete_profile(guild_id: str) -> int:
        """刪除 guild_profiles（FK CASCADE 連帶刪除子資料）。回傳受影響列數。"""
        sql = load_cached_sql("deletes", "guild_profiles_delete.sql")
        return BaseRepository.run_sql_execute(sql, {"guild_id": guild_id})

    # ---------- guild_configs ----------

    @staticmethod
    def upsert_config(
        guild_id: str,
        field_key: str,
        config_value: str | None,
        submitted_at: str,
        updated_at: str,
    ) -> int:
        """新增或更新單一設定。回傳受影響列數。"""
        sql = load_cached_sql("writes", "guild_configs_upsert.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "field_key": field_key,
            "config_value": config_value,
            "submitted_at": submitted_at,
            "updated_at": updated_at,
        })

    @staticmethod
    def get_config(guild_id: str, field_key: str) -> sqlite3.Row | None:
        """讀取單一設定（config_value, submitted_at, updated_at）。"""
        sql = load_cached_sql("reads", "guild_configs_get.sql")
        return BaseRepository.run_sql_fetchone(sql, {
            "guild_id": guild_id,
            "field_key": field_key,
        })

    @staticmethod
    def list_configs(guild_id: str) -> list[sqlite3.Row]:
        """讀取某 guild 的所有設定。"""
        sql = load_cached_sql("reads", "guild_configs_list_by_guild.sql")
        return BaseRepository.run_sql_fetchall(sql, {"guild_id": guild_id})

    @staticmethod
    def delete_config(guild_id: str, field_key: str) -> int:
        """刪除單一設定。回傳受影響列數。"""
        sql = load_cached_sql("deletes", "guild_configs_delete.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "field_key": field_key,
        })
