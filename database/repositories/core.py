# -*- coding: utf-8 -*-
"""
@File    : core.py
@Time    : 2026/6/4 上午 01:55
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

__all__ = ["BaseRepository"]

import sqlite3
from database.connection import get_discord_database_connection


class BaseRepository:

    @staticmethod
    def run_sql_execute(sql_content, parameters=()) -> sqlite3.Cursor:
        cursor: sqlite3.Cursor
        with get_discord_database_connection() as conn:
            cursor = conn.execute(sql_content, parameters)
            conn.commit()
        return cursor



















