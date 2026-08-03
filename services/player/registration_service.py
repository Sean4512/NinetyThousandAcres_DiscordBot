# -*- coding: utf-8 -*-
"""
@File    : registration_service.py
@Time    : 2026/8/3 下午 03:36
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

# services/player/registration_service.py
import sqlite3

from database.repositories import PlayerProfileRepository
from services._base import BaseService
from utils.models.questionnaire import Questionnaire
from utils.exceptions.service_exceptions import (
    PlayerAlreadyRegisteredError,
    PlayerNotRegisteredError,
)


class PlayerRegistrationService(BaseService):

    # ---------- 1. 確認是否已註冊 ----------
    @staticmethod
    def is_registered(guild_id: int, discord_id: int) -> bool:
        """此玩家在該 guild 是否已註冊（已建立 player_profiles）。"""
        return PlayerProfileRepository.exists_profile(str(guild_id), str(discord_id))

    # ---------- 2. 註冊 ----------
    @classmethod
    def register(
        cls,
        guild_id: int,
        discord_id: int,
        questionnaire: Questionnaire,
        answers: dict[str, str | None],
    ) -> None:
        """
        註冊一位玩家：建立 player_profiles，並寫入問卷答案。

        :param answers: field_key -> 答案（通常來自 QuestionnaireResult.answers）
        :raises PlayerAlreadyRegisteredError: 此玩家已註冊
        """
        guild_id_str = str(guild_id)
        discord_id_str = str(discord_id)
        now = cls._now()

        try:
            PlayerProfileRepository.insert_profile(
                guild_id_str, discord_id_str, submitted_at=now
            )
        except sqlite3.IntegrityError as exc:
            raise PlayerAlreadyRegisteredError() from exc

        cls._write_answers(guild_id_str, discord_id_str, questionnaire, answers, now)

    # ---------- 3. 讀取填寫過的問卷 ----------
    @classmethod
    def get_registration(cls, guild_id: int, discord_id: int) -> dict | None:
        """
        讀取玩家 profile + 所有答案；未註冊回傳 None。

        回傳 {"profile": {...}, "answers": {field_key: {field_label, answer, ...}}}
        """
        guild_id_str = str(guild_id)
        discord_id_str = str(discord_id)

        profile = PlayerProfileRepository.get_profile(guild_id_str, discord_id_str)
        if profile is None:
            return None

        rows = PlayerProfileRepository.list_answers(guild_id_str, discord_id_str)
        answers = {row["field_key"]: cls._row_to_dict(row) for row in rows}
        return {"profile": cls._row_to_dict(profile), "answers": answers}

    @classmethod
    def get_answers_map(cls, guild_id: int, discord_id: int) -> dict[str, str] | None:
        """
        讀取玩家所有答案，扁平化為 {field_key: answer}；未註冊回傳 None。
        """
        data = cls.get_registration(guild_id, discord_id)
        if data is None:
            return None
        return {
            field_key: field["answer"]
            for field_key, field in data["answers"].items()
        }

    # ---------- 4. 更新答案 ----------
    @classmethod
    def update_answers(
        cls,
        guild_id: int,
        discord_id: int,
        questionnaire: Questionnaire,
        answers: dict[str, str | None],
    ) -> None:
        """
        更新玩家問卷答案（玩家必須已註冊）。

        :raises PlayerNotRegisteredError: 此玩家尚未註冊
        """
        guild_id_str = str(guild_id)
        discord_id_str = str(discord_id)
        if not PlayerProfileRepository.exists_profile(guild_id_str, discord_id_str):
            raise PlayerNotRegisteredError()

        cls._write_answers(
            guild_id_str, discord_id_str, questionnaire, answers, cls._now()
        )

    # ---------- 選配：取消註冊 ----------
    @staticmethod
    def unregister(guild_id: int, discord_id: int) -> None:
        """移除玩家 profile（FK CASCADE 連帶刪除其答案）。"""
        affected = PlayerProfileRepository.delete_profile(str(guild_id), str(discord_id))
        if affected == 0:
            raise PlayerNotRegisteredError()

    # ---------- 內部：把 answers 寫進 DB（解析 field_label） ----------
    @staticmethod
    def _write_answers(
        guild_id_str: str,
        discord_id_str: str,
        questionnaire: Questionnaire,
        answers: dict[str, str | None],
        now: str,
    ) -> None:
        labels = {f.key: f.label for f in questionnaire.fields}
        for field_key, answer in answers.items():
            PlayerProfileRepository.upsert_answer(
                guild_id=guild_id_str,
                discord_id=discord_id_str,
                field_key=field_key,
                field_label=labels.get(field_key, field_key),
                answer=answer,
                submitted_at=now,
                updated_at=now,
            )






