# -*- coding: utf-8 -*-
"""
@File    : _base.py
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : Repository 共用工具：帶快取的 SQL 檔載入器
"""

from functools import lru_cache

from database.database import load_sql


@lru_cache(maxsize=None)
def load_cached_sql(category: str, filename: str) -> str:
    """
    讀取並快取 SQL 檔內容（同一支檔案只讀一次磁碟）

    :param category: 子資料夾，例如 "reads" / "writes" / "deletes"
    :param filename: SQL 檔名，例如 "read_guild_profile.sql"
    """
    return load_sql(category, filename)
