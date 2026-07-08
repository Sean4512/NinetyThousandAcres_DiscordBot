# -*- coding: utf-8 -*-
"""
@File    : init_db.py
@Time    : 2026/4/14 下午 02:07
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from database.repositories.core import BaseRepository
from utils.sql_loader import load_sql


G_CREATE_TABLE_SQL_FILES = [
    "create_guild_profiles.sql",
    "create_guild_configs.sql",
    "create_player_profiles.sql",
    "create_player_profile_answers.sql",
    "create_match_signup_forms.sql",
    "create_match_signup_forms_participants.sql",
    "create_match_signup_forms_answers.sql",
]

def get_sql_files():
    return G_CREATE_TABLE_SQL_FILES


def init_discord_database() -> None:
    for sql_file in get_sql_files():
        sql_content = load_sql("create", sql_file)
        try:
            BaseRepository.run_sql_execute(sql_content)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize the database({sql_file}): {e}") from e


def init_db() -> None:
    init_discord_database()
