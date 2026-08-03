# -*- coding: utf-8 -*-
"""
@File    : guild_service.py
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : Guild 初始化與設定的商業邏輯層（cog 與 GuildProfileRepository 之間的中間層）。
"""

import sqlite3
from typing import Any

from database.repositories import GuildProfileRepository

from services._base import BaseService
from utils.exceptions.service_exceptions import (
    GuildAlreadySetupError,
    GuildNotSetupError,
)


class GuildConfigKeys:
    """guild_configs.field_key 的合法鍵值；cog 與 service 共用，避免字串散落。"""
    ADMIN_ROLE_ID = "admin_role_id"
    CATEGORY_ID = "category_id"
    REGISTRATION_FORUM_ID = "registration_forum_id"


class GuildService(BaseService):

    @staticmethod
    def is_initialized(guild_id: int) -> bool:
        """此 guild 是否已初始化（已建立 guild_profiles）。"""
        return GuildProfileRepository.exists_profile(str(guild_id))

    @classmethod
    def initialize_guild(
        cls,
        guild_id: int,
        configs: dict[str, str | None],
    ) -> None:
        """
        初始化一個 guild：建立 guild_profiles，並寫入一組初始設定。

        :param guild_id: Discord guild id
        :param configs: field_key -> config_value 的初始設定（例如 admin_role_id）
        :raises GuildAlreadySetupError: 此 guild 已經初始化過
        """
        guild_id_str = str(guild_id)
        now = cls._now()

        try:
            GuildProfileRepository.insert_profile(guild_id_str, submitted_at=now)
        except sqlite3.IntegrityError as exc:
            raise GuildAlreadySetupError() from exc

        # 註：BaseRepository 每次呼叫各自開關連線，此處並非單一交易。
        for field_key, config_value in configs.items():
            GuildProfileRepository.upsert_config(
                guild_id=guild_id_str,
                field_key=field_key,
                config_value=config_value,
                submitted_at=now,
                updated_at=now,
            )

    @classmethod
    def get_profile(cls, guild_id: int) -> dict[str, Any] | None:
        """讀取 guild profile；不存在回傳 None。"""
        row = GuildProfileRepository.get_profile(str(guild_id))
        return cls._row_to_dict(row)

    @classmethod
    def set_config(
        cls,
        guild_id: int,
        field_key: str,
        config_value: str | None,
    ) -> None:
        """
        新增或更新單一設定（guild 必須已初始化）。

        :raises GuildNotSetupError: 此 guild 尚未初始化
        """
        guild_id_str = str(guild_id)
        if not GuildProfileRepository.exists_profile(guild_id_str):
            raise GuildNotSetupError()

        now = cls._now()
        GuildProfileRepository.upsert_config(
            guild_id=guild_id_str,
            field_key=field_key,
            config_value=config_value,
            submitted_at=now,
            updated_at=now,
        )

    @classmethod
    def get_config_value(cls, guild_id: int, field_key: str) -> str | None:
        """讀取單一設定值；設定不存在回傳 None。"""
        row = GuildProfileRepository.get_config(str(guild_id), field_key)
        return row["config_value"] if row is not None else None

    @classmethod
    def get_all_configs(cls, guild_id: int) -> dict[str, str | None]:
        """讀取某 guild 的所有設定，攤平成 field_key -> config_value 的 dict。"""
        rows = GuildProfileRepository.list_configs(str(guild_id))
        return {row["field_key"]: row["config_value"] for row in rows}

    @classmethod
    def remove_guild(cls, guild_id: int) -> None:
        """
        移除整個 guild（FK CASCADE 連帶刪除其設定與子資料）。

        :raises GuildNotSetupError: 此 guild 尚未初始化
        """
        affected = GuildProfileRepository.delete_profile(str(guild_id))
        if affected == 0:
            raise GuildNotSetupError()
