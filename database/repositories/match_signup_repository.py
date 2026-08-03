# -*- coding: utf-8 -*-
"""
@File    : match_signup_repository.py
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : match_signup_forms / participants / player_answers 的資料庫操作
"""

import sqlite3

from database.core import BaseRepository
from database.repositories._base import load_cached_sql


class MatchSignupRepository:

    # ---------- match_signup_forms ----------

    @staticmethod
    def insert_form(
        guild_id: str,
        forum_id: str,
        thread_id: str,
        message_id: str,
        status: str,
        title: str,
        content: str | None,
        log: str | None,
        submitted_at: str,
        updated_at: str,
    ) -> int:
        """新增報名表單（已存在會拋 IntegrityError）。回傳受影響列數。"""
        sql = load_cached_sql("writes", "match_signup_forms_insert.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "forum_id": forum_id,
            "thread_id": thread_id,
            "message_id": message_id,
            "status": status,
            "title": title,
            "content": content,
            "log": log,
            "submitted_at": submitted_at,
            "updated_at": updated_at,
        })

    @staticmethod
    def update_form(
        guild_id: str,
        thread_id: str,
        message_id: str,
        status: str,
        title: str,
        content: str | None,
        log: str | None,
        updated_at: str,
    ) -> int:
        """更新報名表單的可變欄位。回傳受影響列數。"""
        sql = load_cached_sql("writes", "match_signup_forms_update.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
            "message_id": message_id,
            "status": status,
            "title": title,
            "content": content,
            "log": log,
            "updated_at": updated_at,
        })

    @staticmethod
    def update_form_status(
        guild_id: str, thread_id: str, status: str, updated_at: str
    ) -> int:
        """只更新報名表單的 status。回傳受影響列數。"""
        sql = load_cached_sql("writes", "match_signup_forms_update_status.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
            "status": status,
            "updated_at": updated_at,
        })

    @staticmethod
    def get_form(guild_id: str, thread_id: str) -> sqlite3.Row | None:
        """讀取單一報名表單。"""
        sql = load_cached_sql("reads", "match_signup_forms_get.sql")
        return BaseRepository.run_sql_fetchone(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
        })

    @staticmethod
    def list_forms(guild_id: str) -> list[sqlite3.Row]:
        """讀取某 guild 的所有報名表單。"""
        sql = load_cached_sql("reads", "match_signup_forms_list_by_guild.sql")
        return BaseRepository.run_sql_fetchall(sql, {"guild_id": guild_id})

    @staticmethod
    def exists_form(guild_id: str, thread_id: str) -> bool:
        """檢查報名表單是否存在。"""
        sql = load_cached_sql("reads", "match_signup_forms_exists.sql")
        row = BaseRepository.run_sql_fetchone(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
        })
        return bool(row["is_exists"]) if row else False

    @staticmethod
    def delete_form(guild_id: str, thread_id: str) -> int:
        """刪除報名表單（FK CASCADE 連帶刪除 participants 與 answers）。回傳受影響列數。"""
        sql = load_cached_sql("deletes", "match_signup_forms_delete.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
        })

    # ---------- match_signup_forms_participants ----------

    @staticmethod
    def insert_participant(
        guild_id: str, thread_id: str, discord_id: str, submitted_at: str
    ) -> int:
        """新增參與者（已存在會拋 IntegrityError）。回傳受影響列數。"""
        sql = load_cached_sql("writes", "match_signup_forms_participants_insert.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
            "discord_id": discord_id,
            "submitted_at": submitted_at,
        })

    @staticmethod
    def get_participant(
        guild_id: str, thread_id: str, discord_id: str
    ) -> sqlite3.Row | None:
        """讀取單一參與者（submitted_at）。"""
        sql = load_cached_sql("reads", "match_signup_forms_participants_get.sql")
        return BaseRepository.run_sql_fetchone(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
            "discord_id": discord_id,
        })

    @staticmethod
    def list_participants(guild_id: str, thread_id: str) -> list[sqlite3.Row]:
        """讀取某報名表的所有參與者。"""
        sql = load_cached_sql("reads", "match_signup_forms_participants_list.sql")
        return BaseRepository.run_sql_fetchall(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
        })

    @staticmethod
    def exists_participant(guild_id: str, thread_id: str, discord_id: str) -> bool:
        """檢查參與者是否已報名。"""
        sql = load_cached_sql("reads", "match_signup_forms_participants_exists.sql")
        row = BaseRepository.run_sql_fetchone(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
            "discord_id": discord_id,
        })
        return bool(row["is_exists"]) if row else False

    @staticmethod
    def delete_participant(guild_id: str, thread_id: str, discord_id: str) -> int:
        """刪除參與者（FK CASCADE 連帶刪除其 answers）。回傳受影響列數。"""
        sql = load_cached_sql("deletes", "match_signup_forms_participants_delete.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
            "discord_id": discord_id,
        })

    # ---------- match_signup_forms_player_answers ----------

    @staticmethod
    def upsert_answer(
        guild_id: str,
        thread_id: str,
        discord_id: str,
        field_key: str,
        answer: str | None,
        submitted_at: str,
        updated_at: str,
    ) -> int:
        """新增或更新單一回答。回傳受影響列數。"""
        sql = load_cached_sql("writes", "match_signup_forms_answers_upsert.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
            "discord_id": discord_id,
            "field_key": field_key,
            "answer": answer,
            "submitted_at": submitted_at,
            "updated_at": updated_at,
        })

    @staticmethod
    def get_answer(
        guild_id: str, thread_id: str, discord_id: str, field_key: str
    ) -> sqlite3.Row | None:
        """讀取單一回答（answer, submitted_at, updated_at）。"""
        sql = load_cached_sql("reads", "match_signup_forms_answers_get.sql")
        return BaseRepository.run_sql_fetchone(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
            "discord_id": discord_id,
            "field_key": field_key,
        })

    @staticmethod
    def list_answers(
        guild_id: str, thread_id: str, discord_id: str
    ) -> list[sqlite3.Row]:
        """讀取某參與者在某報名表的所有回答。"""
        sql = load_cached_sql("reads", "match_signup_forms_answers_list.sql")
        return BaseRepository.run_sql_fetchall(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
            "discord_id": discord_id,
        })

    @staticmethod
    def delete_answer(
        guild_id: str, thread_id: str, discord_id: str, field_key: str
    ) -> int:
        """刪除單一回答。回傳受影響列數。"""
        sql = load_cached_sql("deletes", "match_signup_forms_answers_delete.sql")
        return BaseRepository.run_sql_execute(sql, {
            "guild_id": guild_id,
            "thread_id": thread_id,
            "discord_id": discord_id,
            "field_key": field_key,
        })
