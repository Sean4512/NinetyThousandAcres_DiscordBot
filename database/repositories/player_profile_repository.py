# -*- coding: utf-8 -*-
"""
@File    : player_profile_repository.py
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : player_profiles 與 player_profiles_answers 的資料庫操作
"""

import sqlite3

from database.core import BaseRepository
from database.repositories._base import load_cached_sql


class PlayerProfileRepository:

    # ---------- player_profiles ----------

    @staticmethod
    def insert_profile(guild_id: str, discord_id: str, submitted_at: str) -> int:
        """新增玩家 profile（已存在會拋 IntegrityError）。回傳受影響列數。"""
        sql = load_cached_sql("writes", "player_profiles_insert.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "discord_id": discord_id,
            "submitted_at": submitted_at,
        })

    @staticmethod
    def get_profile(guild_id: str, discord_id: str) -> sqlite3.Row | None:
        """讀取單一玩家 profile（submitted_at）。"""
        sql = load_cached_sql("reads", "player_profiles_get.sql")
        return BaseRepository.run_sql_fetchone(sql, {
            "guild_id": guild_id,
            "discord_id": discord_id,
        })

    @staticmethod
    def list_profiles(guild_id: str) -> list[sqlite3.Row]:
        """讀取某 guild 的所有玩家。"""
        sql = load_cached_sql("reads", "player_profiles_list_by_guild.sql")
        return BaseRepository.run_sql_fetchall(sql, {"guild_id": guild_id})

    @staticmethod
    def exists_profile(guild_id: str, discord_id: str) -> bool:
        """檢查玩家 profile 是否存在。"""
        sql = load_cached_sql("reads", "player_profiles_exists.sql")
        row = BaseRepository.run_sql_fetchone(sql, {
            "guild_id": guild_id,
            "discord_id": discord_id,
        })
        return bool(row["is_exists"]) if row else False

    @staticmethod
    def delete_profile(guild_id: str, discord_id: str) -> int:
        """刪除玩家 profile（FK CASCADE 連帶刪除其 answers）。回傳受影響列數。"""
        sql = load_cached_sql("deletes", "player_profiles_delete.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "discord_id": discord_id,
        })

    # ---------- player_profiles_answers ----------

    @staticmethod
    def upsert_answer(
        guild_id: str,
        discord_id: str,
        field_key: str,
        field_label: str,
        answer: str | None,
        submitted_at: str,
        updated_at: str,
    ) -> int:
        """新增或更新單一回答。回傳受影響列數。"""
        sql = load_cached_sql("writes", "player_profiles_answers_upsert.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "discord_id": discord_id,
            "field_key": field_key,
            "field_label": field_label,
            "answer": answer,
            "submitted_at": submitted_at,
            "updated_at": updated_at,
        })

    @staticmethod
    def get_answer(guild_id: str, discord_id: str, field_key: str) -> sqlite3.Row | None:
        """讀取單一回答（field_label, answer, submitted_at, updated_at）。"""
        sql = load_cached_sql("reads", "player_profiles_answers_get.sql")
        return BaseRepository.run_sql_fetchone(sql, {
            "guild_id": guild_id,
            "discord_id": discord_id,
            "field_key": field_key,
        })

    @staticmethod
    def list_answers(guild_id: str, discord_id: str) -> list[sqlite3.Row]:
        """讀取某玩家的所有回答。"""
        sql = load_cached_sql("reads", "player_profiles_answers_list.sql")
        return BaseRepository.run_sql_fetchall(sql, {
            "guild_id": guild_id,
            "discord_id": discord_id,
        })

    @staticmethod
    def delete_answer(guild_id: str, discord_id: str, field_key: str) -> int:
        """刪除單一回答。回傳受影響列數。"""
        sql = load_cached_sql("deletes", "player_profiles_answers_delete.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "discord_id": discord_id,
            "field_key": field_key,
        })
