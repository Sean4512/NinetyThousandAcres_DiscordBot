# -*- coding: utf-8 -*-
"""
@File    : match_signup_repository.py
@Time    : 2026/6/18 上午 03:42
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from database.repositories.core import BaseRepository

from utils.sql_loader import load_sql


class MatchSignupRepository(BaseRepository):
    _sql_insert_match_signup_forms = load_sql("sert", "insert_match_signup_forms.sql")
    _sql_get_by_id = load_sql("queries", "get_match_signup_forms_by_id.sql")

    @classmethod
    def insert_match_signup_forms(
        cls,
        guild_id: str,
        forum_id: str,
        thread_id: str,
        message_id: str,
        status: str,
        title: str,
        content: str,
        log: str,
        created_at: str,
        updated_at: str,
    ):

        cls.run_sql_execute(
            cls._sql_insert_match_signup_forms,
            (
                guild_id,
                forum_id,
                thread_id,
                message_id,
                status,
                title,
                content,
                log,
                created_at,
                updated_at
            )
        )

    @classmethod
    def get_match_signup_forms(
        cls,
        guild_id: str,
        thread_id: str,
    ) -> dict[str, str]:
        cursor = cls.run_sql_execute(cls._sql_get_by_id, (guild_id, thread_id))
        row = cursor.fetchone()
        if not row:
            return {}

        result = {
            "forum_id": row["forum_id"],
            "message_id": row["message_id"],
            "status": row["status"],
            "title": row["title"],
            "content": row["content"],
            "log": row["log"],
        }

        return result



class MatchSignupParticipantsRepository(BaseRepository):
    _sql_insert_participants = load_sql("sert", "insert_match_signup_forms_participants.sql")
    _sql_insert_player_answers = load_sql("sert", "insert_match_signup_forms_player_answers.sql")
    _sql_exists_participants = load_sql("queries", "exists_match_signup_forms_participants_by_id.sql")
    _sql_get_participants_answers_by_id = load_sql("queries", "get_match_signup_forms_player_answers.sql")
    _sql_delete_participants_by_id = load_sql("delete", "delete_match_signup_forms_participants.sql")
    _sql_get_participants_by_id = load_sql("queries", "get_match_signup_forms_participants_by_id.sql")

    @classmethod
    def insert_match_signup_forms_participants(
            cls,
            guild_id: str,
            thread_id: str,
            discord_id: str,
            created_at: str
    ):
        cls.run_sql_execute(
            cls._sql_insert_participants,
            (
                guild_id,
                thread_id,
                discord_id,
                created_at
            )
        )

    @classmethod
    def insert_match_signup_forms_player_answers(
            cls,
            guild_id: str,
            thread_id: str,
            discord_id: str,
            field_key: str,
            answer: str,
            created_at: str,
            updated_at: str
    ):
        cls.run_sql_execute(
            cls._sql_insert_player_answers,
            (
                guild_id,
                thread_id,
                discord_id,
                field_key,
                answer,
                created_at,
                updated_at
            )
        )

    @classmethod
    def is_exists(
        cls,
        guild_id: str,
        thread_id: str,
        discord_id: str,
    ):
        cursor = cls.run_sql_execute(cls._sql_exists_participants, (guild_id,thread_id,discord_id))
        row = cursor.fetchone()
        return bool(row[0]) if row is not None else False

    @classmethod
    def get_answers_by_id(
        cls,
        guild_id: str,
        thread_id: str,
        discord_id: str,
    ) -> dict[str, str]:
        cursor = cls.run_sql_execute(
            cls._sql_get_participants_answers_by_id,
            (
                guild_id,
                thread_id,
                discord_id
            )
        )
        rows = cursor.fetchall()
        answers = {row["field_key"]: (row["answer"] if row["answer"] is not None else "") for row in rows}

        return answers

    @classmethod
    def delete_participants_by_id(
        cls,
        guild_id: str,
        thread_id: str,
        discord_id: str,
    ):
        cls.run_sql_execute(
            cls._sql_delete_participants_by_id,
            (
                guild_id,
                thread_id,
                discord_id
            )
        )

    @classmethod
    def get_participants_by_id(
        cls,
        guild_id: str,
        thread_id: str,
    ) -> list[str]:
        cursor = cls.run_sql_execute(
            cls._sql_get_participants_by_id,
            (
                guild_id,
                thread_id
            )
        )
        rows = cursor.fetchall()
        return [row["discord_id"] for row in rows]



