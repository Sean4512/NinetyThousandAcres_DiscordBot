# -*- coding: utf-8 -*-
"""
@File    : match_signup_service.py
@Time    : 2026/6/17 下午 05:21
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations
from datetime import datetime, timezone

import discord

from .guild_service import GuildService
from database.repositories.match_signup_repository import MatchSignupRepository, MatchSignupParticipantsRepository

from utils.Types.questionnaire import QuestionnaireResult
from utils.exceptions.discord_exceptions import (
    DebugError,
    GuildNotInitializedError, InternalError, GuildOnlyError, PlayerNoRegisteredError, ParameterError
)

class MatchSignupService:

    @staticmethod
    async def get_registration_forum(
        guild: discord.Guild,
        registration_forum_id: str | int,
    ) -> discord.ForumChannel | None:
        try:
            forum_id = int(registration_forum_id)
        except (TypeError, ValueError):
            return None

        channel = guild.get_channel(forum_id)

        if channel is None:
            try:
                # 快取不存在時，向 Discord API 查詢
                channel = await guild.fetch_channel(forum_id)

            except discord.NotFound:
                # 頻道不存在或已被刪除
                return None

            except discord.Forbidden:
                # Bot 沒有查看該頻道的權限
                return None

            except discord.HTTPException:
                # Discord API 呼叫失敗
                return None

            # 防止資料庫中的 ID 指向另一個伺服器的頻道
        if channel.guild.id != guild.id:
            return None

        if not isinstance(channel, discord.ForumChannel):
            return None

        return channel


    @staticmethod
    def insert_match_signup_forms(
        guild_id: str,
        forum_id: str,
        thread_id: str,
        message_id: str,
        status: str | None,
        title: str | None,
        content: str | None,
        log: str,
    ) -> tuple[bool, str]:
        now = datetime.now(timezone.utc).isoformat()

        match_signup_info = MatchSignupRepository.get_match_signup_forms(guild_id, thread_id)

        print(
            f"Database insert failed."
            f"guild_id={guild_id}, forum_id={str(forum_id)}, "
            f"thread_id={str(thread_id)}, message_id={str(message_id)}, "
            f"title=\"{title}\", content=\"{content}\"")

        if match_signup_info:
            status = status if status is not None else match_signup_info.get("status", "")
            title = title if title is not None else match_signup_info.get("title", "")
            content = content if content is not None else match_signup_info.get("content", "")
            log = match_signup_info.get("log", "") + log

        content = content if content else ""

        print(
            f"Database insert failed."
            f"guild_id={guild_id}, forum_id={str(forum_id)}, "
            f"thread_id={str(thread_id)}, message_id={str(message_id)}, "
            f"title=\"{title}\", content=\"{content}\"")

        if status is None or title is None or content is None:
            return False, "資料更新失敗。"

        print(
            f"Database insert failed."
            f"guild_id={guild_id}, forum_id={str(forum_id)}, "
            f"thread_id={str(thread_id)}, message_id={str(message_id)}, "
            f"title=\"{title}\", content=\"{content}\"")

        MatchSignupRepository.insert_match_signup_forms(
            guild_id=guild_id,
            forum_id=forum_id,
            thread_id=thread_id,
            message_id=message_id,
            status=status,
            title=title,
            content=content,
            log=log,
            created_at=now,
            updated_at=now,
        )

        return True, "資料更新完成。"


    @staticmethod
    def insert_match_signup_forms_participants(
        guild_id: str,
        thread_id: str,
        discord_id: str,
    ) -> tuple[bool, str]:
        now = datetime.now(timezone.utc).isoformat()
        MatchSignupParticipantsRepository.insert_match_signup_forms_participants(
            guild_id=guild_id,
            thread_id=thread_id,
            discord_id=discord_id,
            created_at=now,
        )

        return True, "資料更新完成。"

    @staticmethod
    def insert_match_signup_forms_player_answers(
        guild_id: str,
        thread_id: str,
        discord_id: str,
        answers: dict[str, str],
        is_update: bool = False
    ) -> tuple[bool, str]:
        now = datetime.now(timezone.utc).isoformat()

        for field_key, answer in answers.items():
            MatchSignupParticipantsRepository.insert_match_signup_forms_player_answers(
                guild_id=guild_id,
                thread_id=thread_id,
                discord_id=discord_id,
                field_key=field_key,
                answer=answer,
                created_at=now,
                updated_at=now,
            )

        return True, "資料更新完成。"

    @staticmethod
    def signup_player(
        guild_id: str,
        thread_id: str,
        discord_id: str,
        answers: dict[str, str],
        is_update: bool = False
    ) -> tuple[bool, str]:

        # is_exists = MatchSignupService.is_exists_match_signup_for_participants(
        #     guild_id=guild_id,
        #     thread_id=thread_id,
        #     discord_id=discord_id,
        # )
        # if not is_exists:
        success, message = MatchSignupService.insert_match_signup_forms_participants(
            guild_id=guild_id,
            thread_id=thread_id,
            discord_id=discord_id,
        )

        if not success:
            return success, message

        success, message = MatchSignupService.insert_match_signup_forms_player_answers(
            guild_id=guild_id,
            thread_id=thread_id,
            discord_id=discord_id,
            answers=answers,
            is_update=is_update
        )
        return success, message


    @staticmethod
    def is_exists_match_signup_for_participants(
        guild_id: str,
        thread_id: str,
        discord_id: str,
    ) -> bool:
        return MatchSignupParticipantsRepository.is_exists(
            guild_id=guild_id,
            thread_id=thread_id,
            discord_id=discord_id,
        )

    @staticmethod
    def get_participants_answers_by_id(
        guild_id: str,
        thread_id: str,
        discord_id: str,
    ) -> dict[str, str]:
        return MatchSignupParticipantsRepository.get_answers_by_id(
            guild_id=guild_id,
            thread_id=thread_id,
            discord_id=discord_id,
        )

    @staticmethod
    def delete_participants_by_id(
        guild_id: str,
        thread_id: str,
        discord_id: str,
    ):
        MatchSignupParticipantsRepository.delete_participants_by_id(
            guild_id=guild_id,
            thread_id=thread_id,
            discord_id=discord_id,
        )

    @staticmethod
    def get_participants_by_id(
        guild_id: str,
        thread_id: str,
    ) -> list[str]:
        return MatchSignupParticipantsRepository.get_participants_by_id(
            guild_id=guild_id,
            thread_id=thread_id,
        )
