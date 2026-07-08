# -*- coding: utf-8 -*-
"""
@File    : connection.py
@Time    : 2026/4/14 下午 01:52
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import sqlite3
from pathlib import Path

from config.settings import get_database_settings

__all__ = ["get_discord_database_connection"]


try:
    g_database_directory = Path(get_database_settings().DIRECTORY)
    g_discord_guild_database_path = g_database_directory / get_database_settings().DISCORD_FILE
except Exception as e:
    raise RuntimeError(f"Failed to load database settings: {e}") from e

def get_discord_database_connection() -> sqlite3.Connection:
    try:
        g_database_directory.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(g_discord_guild_database_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    except sqlite3.Error as e:
        raise RuntimeError(
            f"Failed to connect to SQLite database: path={g_discord_guild_database_path}, error={e}"
        ) from e

    except OSError as e:
        raise RuntimeError(
            f"Failed to create database directory: path={g_database_directory}, error={e}"
        ) from e

    except Exception as e:
        raise RuntimeError(
            f"Unexpected error occurred while creating Discord guild database connection: {e}"
        ) from e





