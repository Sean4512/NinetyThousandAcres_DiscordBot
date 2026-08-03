# -*- coding: utf-8 -*-
"""
@File    : settings.py
@Time    : 2026/6/19 下午 04:04
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations

import os
import inspect
import shutil
from pathlib import Path
from dotenv import load_dotenv


_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_ENV_FILE = _PROJECT_ROOT / ".env"
_ENV_EXAMPLE_FILE = _PROJECT_ROOT / ".env.example"

def ensure_env_file() -> None:
    """
    如果專案根目錄不存在 .env，
    就從 .env.example 複製一份 .env。
    """
    global _ENV_FILE, _ENV_EXAMPLE_FILE
    if _ENV_FILE.exists():
        return

    if not _ENV_EXAMPLE_FILE.exists():
        _ENV_FILE.write_text(
            get_default_env_template(),
            encoding="utf-8",
        )
        return

    shutil.copyfile(_ENV_EXAMPLE_FILE, _ENV_FILE)

ensure_env_file()
load_dotenv(_ENV_FILE)

def get_default_env_template() -> str:
    return """# Discord Bot
NINETY_THOUSAND_ACRES_DISCORD_BOT_TOKEN=
NINETY_THOUSAND_ACRES_DISCORD_BOT_SYNC_COMMANDS=False
NINETY_THOUSAND_ACRES_DISCORD_GUILD_ID_FOR_DEBUG=0
NINETY_THOUSAND_ACRES_DISCORD_BOT_EXTENSIONS_YAML_PATH=./cfg/bot_extensions.yaml
NINETY_THOUSAND_ACRES_DISCORD_BOT_COMMAND_PREFIX=!
NINETY_THOUSAND_ACRES_DISCORD_BOT_PLAYER_REGISTER_TIMEOUT=300

# NTA Config
NINETY_THOUSAND_ACRES_PLAYER_REGISTER_FIELDS_YAML_PATH=./cfg/player_register_fields.yaml
NINETY_THOUSAND_ACRES_MATCH_SIGNUP_REGISTRATION_FIELDS_YAML_PATH=./cfg/match_signup_fields.yaml
NINETY_THOUSAND_ACRES_MATCH_SIGNUP_CREATION_FIELDS_YAML_PATH=./cfg/create_match_signup_fields.yaml

# Logger
NINETY_THOUSAND_ACRES_LOG_DIRECTORY=./logs
NINETY_THOUSAND_ACRES_BOT_LOG_LEVEL=INFO

# Database
NINETY_THOUSAND_ACRES_DATABASE_DIRECTORY=./data/db
NINETY_THOUSAND_ACRES_DATABASE_DISCORD_FILE=discord.db
"""

def getenv_bool(key: str, default: bool = False) -> bool:
    value = os.getenv(key)

    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "t", "yes", "y", "on"}


class SettingBase:
    _SENSITIVE_KEYS = {}

    def __str__(self) -> str:
        # lines = ["Discord bot settings:"]
        lines = [self.__class__.__name__]
        # lines.append(self.__class__.__name__)

        for key, value in self.__class__.__dict__.items():
            if key.startswith("_"):
                continue

            if inspect.isfunction(value) or inspect.ismethod(value):
                continue

            if key in self._SENSITIVE_KEYS:
                lines.append(f"{key}: ********")
                continue

            lines.append(f"{key}: {value}")

        lines.append("\n")
        return "\n".join(lines)

class NtaSettings(SettingBase):
    PLAYER_REGISTER_FIELDS_YAML_PATH: str = os.getenv("NINETY_THOUSAND_ACRES_PLAYER_REGISTER_FIELDS_YAML_PATH", "./cfg/player_register_fields.yaml")
    MATCH_SIGNUP_REGISTRATION_FIELDS_YAML_PATH: str = os.getenv("NINETY_THOUSAND_ACRES_MATCH_SIGNUP_REGISTRATION_FIELDS_YAML_PATH", "./cfg/match_signup_registration_fields.yaml")
    MATCH_SIGNUP_CREATION_FIELDS_YAML_PATH: str = os.getenv("NINETY_THOUSAND_ACRES_MATCH_SIGNUP_CREATION_FIELDS_YAML_PATH", "./cfg/match_signup_creation_fields.yaml")

class LoggerSettings(SettingBase):
    DIRECTORY: str = os.getenv("NINETY_THOUSAND_ACRES_LOG_DIRECTORY", "./logs")

    # CRITICAL, FATAL, ERROR, WARN, WARNING, INFO, DEBUG, NOTSET
    BOT_LEVEL: str = os.getenv("NINETY_THOUSAND_ACRES_BOT_LOG_LEVEL", "INFO")

class DiscordBotSettings(SettingBase):
    BOT_TOKEN: str = os.getenv("NINETY_THOUSAND_ACRES_DISCORD_BOT_TOKEN", "")
    SYNC_COMMANDS: bool = getenv_bool("NINETY_THOUSAND_ACRES_DISCORD_BOT_SYNC_COMMANDS", False)
    GUILD_ID_FOR_DEBUG: int = int(os.getenv("NINETY_THOUSAND_ACRES_DISCORD_GUILD_ID_FOR_DEBUG", "0"))
    EXTENSIONS_YAML_PATH: str = os.getenv("NINETY_THOUSAND_ACRES_DISCORD_BOT_EXTENSIONS_YAML_PATH", "./cfg/bot_extensions.yaml")
    COMMAND_PREFIX: str = os.getenv("NINETY_THOUSAND_ACRES_DISCORD_BOT_COMMAND_PREFIX", "!")
    PLAYER_REGISTER_TIMEOUT: int = int(os.getenv("NINETY_THOUSAND_ACRES_DISCORD_BOT_PLAYER_REGISTER_TIMEOUT", "300"))

    _SENSITIVE_KEYS = {"BOT_TOKEN"}

class DatabaseSettings(SettingBase):
    DIRECTORY: str = os.getenv("NINETY_THOUSAND_ACRES_DATABASE_DIRECTORY", "./data/db")
    DISCORD_FILE: str = os.getenv("NINETY_THOUSAND_ACRES_DATABASE_DISCORD_FILE", "discord.db")


G_NTA_SETTINGS: NtaSettings
G_LOGGER_SETTINGS: LoggerSettings
G_DISCORD_BOT_SETTINGS: DiscordBotSettings
G_DATABASE_SETTINGS: DatabaseSettings

def get_nta_settings() -> NtaSettings:
    global G_NTA_SETTINGS
    if G_NTA_SETTINGS is None:
        raise ValueError("Nta settings not initialized")
    return G_NTA_SETTINGS

def get_logger_settings() -> LoggerSettings:
    global G_LOGGER_SETTINGS
    if G_LOGGER_SETTINGS is None:
        raise ValueError("Logger settings not initialized")
    return G_LOGGER_SETTINGS

def get_discord_bot_settings() -> DiscordBotSettings:
    global G_DISCORD_BOT_SETTINGS
    if G_DISCORD_BOT_SETTINGS is None:
        raise ValueError("Discord bot settings not initialized")
    return G_DISCORD_BOT_SETTINGS

def get_database_settings() -> DatabaseSettings:
    global G_DATABASE_SETTINGS
    if G_DATABASE_SETTINGS is None:
        raise ValueError("Database settings not initialized")
    return G_DATABASE_SETTINGS

def setup_nta_settings():
    global G_NTA_SETTINGS
    G_NTA_SETTINGS = NtaSettings()

def setup_logger_settings():
    global G_LOGGER_SETTINGS
    G_LOGGER_SETTINGS = LoggerSettings()

def setup_discord_bot_settings():
    global G_DISCORD_BOT_SETTINGS
    G_DISCORD_BOT_SETTINGS = DiscordBotSettings()

def setup_database_settings():
    global G_DATABASE_SETTINGS
    G_DATABASE_SETTINGS = DatabaseSettings()

def initialize_settings():
    setup_nta_settings()
    setup_logger_settings()
    setup_discord_bot_settings()
    setup_database_settings()





