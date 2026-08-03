# -*- coding: utf-8 -*-
"""
@File    : database.py
@Time    : 2026/6/30 下午 05:50
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from pathlib import Path

from database.core import BaseRepository


G_SQL_DIRECTORY = Path(__file__).resolve().parent.parent / "database" / "sql"

G_CREATE_TABLE_SQL_FILES = [
    "create_guild_profiles.sql",
    "create_guild_configs.sql",
    "create_player_profiles.sql",
    "create_player_profiles_answers.sql",
    "create_match_signup_forms.sql",
    "create_match_signup_forms_participants.sql",
    "create_match_signup_forms_answers.sql",
]

def load_sql(*relative_parts: str) -> str:
    """
    Load the SQL content

    Example:
        load_sql("guild_config", "create_table.sql")
    """
    sql_file_path = G_SQL_DIRECTORY.joinpath(*relative_parts)

    if not sql_file_path.is_file():
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    return sql_file_path.read_text(encoding="utf-8")

def get_sql_files():
    global G_CREATE_TABLE_SQL_FILES
    for sql_file in G_CREATE_TABLE_SQL_FILES:
        yield sql_file

def setup_discord_database() -> None:
    for sql_file in get_sql_files():
        sql_content = load_sql("create", sql_file)
        try:
            BaseRepository.run_sql_execute(sql_content)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize the database({sql_file}): {e}") from e

def initialize_database() -> None:
    from database.connection import setup_global_parameters
    setup_global_parameters()
    setup_discord_database()
