# -*- coding: utf-8 -*-
"""
@File    : database_types.py
@Time    : 2026/5/8 上午 12:20
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from dataclasses import dataclass


@dataclass(slots=True)
class GuildConfig:
    """
    與 Discord guild database 的資料結構相同
    """
    guild_id: str = ""
    guild_name: str = ""
    is_initialized: int = 0
    admin_role_id: str | None = None
    category_id : str | None = None
    registration_forum_id: str | None = None
    created_at: str = ""
    updated_at: str = ""


@dataclass(slots=True)
class PlayerProfiles:
    """
    與 Discord player_profiles database 的資料結構相同
    """
    discord_id: str = ""
    guild_id: str = ""

    admin_notes: str = ""    # 管理員給予的備註
    created_at: str = ""
    updated_at: str = ""





