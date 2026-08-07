# -*- coding: utf-8 -*-
"""
@File    : form_service.py
@Time    : 2026/8/3 下午 03:36
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from enum import Enum
import sqlite3

from database.repositories import MatchSignupRepository

from services._base import BaseService
from utils.exceptions.service_exceptions import MatchSignupFormAlreadyExistsError, MatchSignupFormNotFoundError


class MatchSignupConfigKeys:
    TITLE = "match_signup_title"
    CONTENT = "match_signup_content"

class MatchSignupThreadStatus(str, Enum):
    # ACTIVE = "active"
    # INACTIVE = "inactive"
    OPEN = "open"
    CLOSED = "closed"

class MatchSignupFormService(BaseService):

    @staticmethod
    def _validate_status(status: MatchSignupThreadStatus) -> None:
        if not isinstance(status, MatchSignupThreadStatus):
            raise TypeError("status 必須是 MatchSignupThreadStatus")

    @staticmethod
    def exists(guild_id: int, thread_id: int,) -> bool:
        return MatchSignupRepository.exists_form(str(guild_id), str(thread_id))

    @classmethod
    def create(
        cls,
        guild_id: int,
        forum_id: int,
        thread_id: int,
        message_id: int,
        status: MatchSignupThreadStatus,
        title: str,
        content: str,
    ) -> None:

        if cls.exists(guild_id, thread_id):
            raise MatchSignupFormAlreadyExistsError()

        cls._validate_status(status)

        if not isinstance(title, str):
            raise TypeError("title 必須是 str")
        elif not isinstance(content, str):
            raise TypeError("content 必須是 str")

        guild_id_str = str(guild_id)
        forum_id_str = str(forum_id)
        thread_id_str = str(thread_id)
        message_id_str = str(message_id)
        now = cls._now()

        try:
            MatchSignupRepository.insert_form(
                guild_id = guild_id_str,
                forum_id = forum_id_str,
                thread_id = thread_id_str,
                message_id = message_id_str,
                status = status.value,
                title = title,
                content = content,
                log=None,
                submitted_at=now,
                updated_at=now,
            )
        except sqlite3.IntegrityError as exc:
            if cls.exists(guild_id, thread_id):
                raise MatchSignupFormAlreadyExistsError() from exc
            raise

    @classmethod
    def update_status(
        cls,
        guild_id: int,
        thread_id: int,
        status: MatchSignupThreadStatus,
    ) -> None:

        if not cls.exists(guild_id, thread_id):
            raise MatchSignupFormNotFoundError()

        cls._validate_status(status)

        guild_id_str = str(guild_id)
        thread_id_str = str(thread_id)
        now = cls._now()

        affected = MatchSignupRepository.update_form_status(
            guild_id = guild_id_str,
            thread_id = thread_id_str,
            status = status.value,
            updated_at=now
        )

        if affected == 0:
            raise MatchSignupFormNotFoundError()

    @classmethod
    def update_details(
        cls,
        guild_id: int,
        thread_id: int,
        message_id: int,
        status: MatchSignupThreadStatus,
        title: str,
        content: str,
    ):
        if not cls.exists(guild_id, thread_id):
            raise MatchSignupFormNotFoundError()

        cls._validate_status(status)

        if not isinstance(title, str):
            raise TypeError("title 必須是 str")
        elif not isinstance(content, str):
            raise TypeError("content 必須是 str")

        guild_id_str = str(guild_id)
        thread_id_str = str(thread_id)
        message_id_str = str(message_id)
        now = cls._now()

        MatchSignupRepository.update_form(
            guild_id = guild_id_str,
            thread_id = thread_id_str,
            message_id = message_id_str,
            status = status.value,
            title = title,
            content = content,
            log = None,
            updated_at=now,
        )

    @classmethod
    def delete(
        cls,
        guild_id: int,
        thread_id: int,
    ):
        if not cls.exists(guild_id, thread_id):
            raise MatchSignupFormNotFoundError()

        guild_id_str = str(guild_id)
        thread_id_str = str(thread_id)

        MatchSignupRepository.delete_form(
            guild_id = guild_id_str,
            thread_id = thread_id_str,
        )




