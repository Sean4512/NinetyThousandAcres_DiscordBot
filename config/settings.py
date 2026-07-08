# -*- coding: utf-8 -*-
"""
@File    : settings.py.py
@Time    : 2026/4/11 上午 02:52
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import os
from dotenv import load_dotenv
import inspect
from distutils.util import strtobool

__all__ = ["get_nta_settings", "get_logger_settings", "get_discord_bot_settings", "get_database_settings"]

load_dotenv()


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
    MATCH_SIGNUP_FIELDS_YAML_PATH: str = os.getenv("NINETY_THOUSAND_ACRES_MATCH_SIGNUP_FIELDS_YAML_PATH", "./cfg/match_signup_fields.yaml")
    CREATE_MATCH_SIGNUP_FIELDS_YAML_PATH: str = os.getenv("NINETY_THOUSAND_ACRES_CREATE_MATCH_SIGNUP_FIELDS_YAML_PATH", "./cfg/create_match_signup_fields.yaml")


class LoggerSettings(SettingBase):
    DIRECTORY: str = os.getenv("NINETY_THOUSAND_ACRES_LOG_DIRECTORY", "./logs")

    # CRITICAL, FATAL, ERROR, WARN, WARNING, INFO, DEBUG, NOTSET
    BOT_LEVEL: str = os.getenv("NINETY_THOUSAND_ACRES_BOT_LOG_LEVEL", "INFO")


class DiscordBotSettings(SettingBase):
    BOT_TOKEN: str = os.getenv("NINETY_THOUSAND_ACRES_DISCORD_BOT_TOKEN", "")
    SYNCED_COMMAND: bool = strtobool(os.getenv("NINETY_THOUSAND_ACRES_DISCORD_BOT_SYNCED_COMMAND", 'False'))
    SYNCED_COMMAND_FOR_DEBUG: bool = strtobool(os.getenv("NINETY_THOUSAND_ACRES_DISCORD_BOT_SYNCED_COMMAND_FOR_DEBUG", 'False'))
    GUILD_ID_FOR_DEBUG: int = int(os.getenv("NINETY_THOUSAND_ACRES_DISCORD_GUILD_ID_FOR_DEBUG", "0"))
    EXTENSIONS_YAML_PATH: str = os.getenv("NINETY_THOUSAND_ACRES_DISCORD_BOT_EXTENSIONS_YAML_PATH", "./cfg/bot_extensions.yaml")
    COMMAND_PREFIX: str = os.getenv("NINETY_THOUSAND_ACRES_DISCORD_BOT_COMMAND_PREFIX", "!")
    PLAYER_REGISTER_TIMEOUT: int = int(os.getenv("NINETY_THOUSAND_ACRES_DISCORD_BOT_PLAYER_REGISTER_TIMEOUT", "300"))

    _SENSITIVE_KEYS = {"BOT_TOKEN"}


class DatabaseSettings(SettingBase):
    DIRECTORY: str = os.getenv("NINETY_THOUSAND_ACRES_DATABASE_DIRECTORY", "./data/db")
    DISCORD_FILE: str = os.getenv("NINETY_THOUSAND_ACRES_DATABASE_DISCORD_FILE", "discord.db")

g_nta_settings = NtaSettings()
g_logger_settings = LoggerSettings()
g_discord_bot_settings = DiscordBotSettings()
g_database_settings = DatabaseSettings()

def get_nta_settings() -> NtaSettings:
    global g_nta_settings
    if g_nta_settings is None:
        raise ValueError("Nta settings not initialized")
    return g_nta_settings

def get_logger_settings() -> LoggerSettings:
    global g_logger_settings
    if g_logger_settings is None:
        raise ValueError("Logger settings not initialized")
    return g_logger_settings

def get_discord_bot_settings() -> DiscordBotSettings:
    global g_discord_bot_settings
    if g_discord_bot_settings is None:
        raise ValueError("Discord bot settings not initialized")
    return g_discord_bot_settings

def get_database_settings() -> DatabaseSettings:
    global g_database_settings
    if g_database_settings is None:
        raise ValueError("Database settings not initialized")
    return g_database_settings
