# -*- coding: utf-8 -*-
"""
@File    : guild_service.py
@Time    : 2026/4/14 下午 09:52
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from datetime import datetime, timezone

from database.repositories.guild_repository import GuildProfileRepository, GuildConfigRepository
from utils.Types.database_types import GuildConfig


class GuildService:

    @staticmethod
    def is_exists(guild_id: str) -> bool:
        return GuildProfileRepository.is_exists(guild_id)

    @staticmethod
    def insert_guild_profile(
        guild_id: str,
    ) -> tuple[bool, str]:
        is_exists = GuildService.is_exists(guild_id)
        if not is_exists:
            now = datetime.now(timezone.utc).isoformat()
            GuildProfileRepository.insert_guild_profile(
                guild_id=guild_id,
                created_at=now
            )
        return True, "此伺服器已完成註冊。"

    @staticmethod
    def upsert_guild_config(
        guild_id: str,
        configs: dict[str, str],
    ) -> tuple[bool, str]:
        is_exists = GuildService.is_exists(guild_id)
        if not is_exists:
            return False, "此伺服器尚未完成初始化，請執行 /setup"

        now = datetime.now(timezone.utc).isoformat()
        GuildConfigRepository.upsert_guild_config(
            guild_id=guild_id,
            configs=configs,
            created_at=now,
            updated_at=now,
        )
        return True, "已完成資料更新"

    @staticmethod
    def get_config_by_id(
        guild_id: str,
    ) -> dict[str, str] | None:
        is_exists = GuildService.is_exists(guild_id)
        if not is_exists:
            return None
        return GuildConfigRepository.get_config_by_id(guild_id=guild_id)

    @staticmethod
    def get_guild_config_by_guild_id(guild_id: str) -> GuildConfig | None:
        configs = GuildService.get_config_by_id(guild_id)
        if configs is None:
            return None

        guild_config = GuildConfig()
        guild_config.guild_id = guild_id
        guild_config.created_at = configs.get("created_at", "")
        guild_config.updated_at = configs.get("updated_at", "")

        guild_config.guild_name = configs.get("guild_name", "")
        guild_config.admin_role_id = configs.get("admin_role_id", "")
        guild_config.category_id = configs.get("category_id", "")
        guild_config.registration_forum_id = configs.get("registration_forum_id", "")

        return guild_config



