# -*- coding: utf-8 -*-
"""
@File    : __init__.py
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : Service 層：bot/commands（cog）與 database/repositories 之間的中間層。

負責商業邏輯編排、時間戳產生、Row -> dict 轉換、DB 例外翻譯成 domain 例外。
之後可依樣新增 PlayerService、MatchSignupService。
"""

from services.guild_service import GuildService, GuildConfigKeys

__all__ = [
    "GuildService",
    "GuildConfigKeys",
]
