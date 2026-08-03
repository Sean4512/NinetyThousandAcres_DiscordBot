# -*- coding: utf-8 -*-
"""
@File    : connection.py
@Time    : 2026/6/30 下午 06:01
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import sqlite3
from pathlib import Path

from config.settings import get_database_settings


G_DATABASE_DIRECTORY: Path
G_DISCORD_GUILD_DATABASE_PATH: Path

def setup_global_parameters() -> None:
    global G_DATABASE_DIRECTORY, G_DISCORD_GUILD_DATABASE_PATH
    try:
        G_DATABASE_DIRECTORY = Path(get_database_settings().DIRECTORY)
        G_DISCORD_GUILD_DATABASE_PATH = G_DATABASE_DIRECTORY / get_database_settings().DISCORD_FILE
    except Exception as e:
        raise RuntimeError(f"Failed to load database settings: {e}") from e


def get_discord_database_connection() -> sqlite3.Connection:
    try:
        G_DATABASE_DIRECTORY.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(G_DISCORD_GUILD_DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    except sqlite3.Error as e:
        raise RuntimeError(
            f"Failed to connect to SQLite database: path={G_DISCORD_GUILD_DATABASE_PATH}, error={e}"
        ) from e

    except OSError as e:
        raise RuntimeError(
            f"Failed to create database directory: path={G_DATABASE_DIRECTORY}, error={e}"
        ) from e

    except Exception as e:
        raise RuntimeError(
            f"Unexpected error occurred while creating Discord guild database connection: {e}"
        ) from e
