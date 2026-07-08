# -*- coding: utf-8 -*-
"""
@File    : sql_loader.py
@Time    : 2026/4/14 下午 06:34
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from pathlib import Path

from utils.paths import g_sql_dir


def load_sql(*relative_parts: str) -> str:
    """
    Load the SQL content

    Example:
        load_sql("guild_config", "create_table.sql")
    """
    sql_file_path = g_sql_dir.joinpath(*relative_parts)

    if not sql_file_path.is_file():
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    return sql_file_path.read_text(encoding="utf-8")


