# -*- coding: utf-8 -*-
"""
@File    : auth_service.py
@Time    : 2026/4/15 上午 01:38
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from typing import Tuple

import discord

from utils.Types.database_types import GuildConfig


class AuthService:
    @staticmethod
    def is_guild_initialized(guild_config: GuildConfig | None) -> bool:
        if guild_config is None:
            return False
        if guild_config.is_initialized != 1:
            return False
        return True

    @staticmethod
    def has_admin_role(guild_config: GuildConfig | None, user_role_ids: list[str]) -> bool:

        assert guild_config is not None

        if guild_config.admin_role_id is None:
            return False

        if guild_config.admin_role_id not in user_role_ids:
            return False

        return True


class DiscordAuthService:

    @staticmethod
    def is_guild(interaction: discord.Interaction) -> Tuple[bool, str | None]:
        if interaction.guild is None:
            return False, "此指令只能在伺服器內使用。"
        return True, None

    @staticmethod
    def check_member(interaction: discord.Interaction) -> tuple[bool, str | None]:
        if not isinstance(interaction.user, discord.Member):
            return False, "無法取得你的伺服器身分組資訊。"
        return True, None














