# -*- coding: utf-8 -*-
"""
@File    : logger.py
@Time    : 2026/6/20 上午 01:38
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import os
from config.settings import get_logger_settings
import logging


_MAIN_LOG_FILE = "main.log"
_DISCORD_BOT_LOG_FILE = "bot.log"
G_MAIN_LOGGER: logging.Logger | None = None
G_DISCORD_BOT_LOGGER: logging.Logger | None = None

def get_main_logger() -> logging.Logger:
    global G_MAIN_LOGGER

    if G_MAIN_LOGGER is None:
        raise ValueError("Main logger not initialized")

    return G_MAIN_LOGGER

def get_discord_bot_logger() -> logging.Logger:
    global G_DISCORD_BOT_LOGGER

    if G_DISCORD_BOT_LOGGER is None:
        raise ValueError("Discord bot logger not initialized")

    return G_DISCORD_BOT_LOGGER

def logger_name_to_level(level):
    name_to_level = {
        'CRITICAL': logging.CRITICAL,
        'FATAL': logging.FATAL,
        'ERROR': logging.ERROR,
        'WARN': logging.WARNING,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.NOTSET,
    }
    return name_to_level[level]

class ColoredFormatter(logging.Formatter):
    RESET = "\033[0m"
    COLORS = {
        "DEBUG": "\033[34m",      # 白色
        "INFO": "\033[32m",       # 綠色
        "WARNING": "\033[33m",    # 黃色
        "ERROR": "\033[31m",      # 紅色
        "CRITICAL": "\033[41m",   # 紅底
        "FATAL": "\033[41m",      # 紅底
    }

    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        color = self.COLORS.get(levelname, self.RESET)

        # 只把 [LEVEL] 這一段上色
        record.colored_levelname = f"{color}{levelname}{self.RESET}"

        return super().format(record)

def setup_main_logger():

    logger_settings = get_logger_settings()
    # 確保log存入指定資料夾
    if not os.path.isdir(logger_settings.DIRECTORY):
        os.makedirs(logger_settings.DIRECTORY, exist_ok=True)

    # 避免資料夾建立失敗
    if not os.path.isdir(logger_settings.DIRECTORY):
        raise ValueError("Logger directory not initialized")

    global _MAIN_LOG_FILE, G_MAIN_LOGGER
    G_MAIN_LOGGER = logging.getLogger("main")
    if G_MAIN_LOGGER is None:
        raise ValueError("Logger not initialized")
    G_MAIN_LOGGER.setLevel(logging.INFO)

    if not G_MAIN_LOGGER.handlers:
        normal_formatter = logging.Formatter(
            fmt="[%(asctime)s][%(name)s][%(levelname)s] %(message)s \t(%(filename)s:%(lineno)d)",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        color_formatter = ColoredFormatter(
            fmt="[%(asctime)s][%(name)s][%(colored_levelname)s] %(message)s \t(%(filename)s:%(lineno)d)",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 輸出到終端機
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(color_formatter)
        G_MAIN_LOGGER.addHandler(console_handler)

        # 輸出到檔案
        file_handler = logging.FileHandler(
            os.path.join(logger_settings.DIRECTORY, _MAIN_LOG_FILE),
            encoding="utf-8"
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(normal_formatter)
        G_MAIN_LOGGER.addHandler(file_handler)

def setup_discord_bot_logger():
    logger_settings = get_logger_settings()

    global _DISCORD_BOT_LOG_FILE, G_DISCORD_BOT_LOGGER
    G_DISCORD_BOT_LOGGER = logging.getLogger("discord_bot")
    if G_DISCORD_BOT_LOGGER is None:
        raise ValueError("Discord bot logger not initialized")
    G_DISCORD_BOT_LOGGER.setLevel(logger_name_to_level(logger_settings.BOT_LEVEL))

    if not G_DISCORD_BOT_LOGGER.handlers:
        normal_formatter = logging.Formatter(
            fmt="[%(asctime)s][%(name)s][%(levelname)s] %(message)s \t(%(filename)s:%(lineno)d)",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        color_formatter = ColoredFormatter(
            fmt="[%(asctime)s][%(name)s][%(colored_levelname)s] %(message)s \t(%(filename)s:%(lineno)d)",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 輸出到終端機
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logger_name_to_level(logger_settings.BOT_LEVEL))
        console_handler.setFormatter(color_formatter)
        G_DISCORD_BOT_LOGGER.addHandler(console_handler)

        # 輸出到檔案
        file_handler = logging.FileHandler(
            os.path.join(logger_settings.DIRECTORY, _DISCORD_BOT_LOG_FILE),
            encoding="utf-8"
        )
        file_handler.setLevel(logger_name_to_level(logger_settings.BOT_LEVEL))
        file_handler.setFormatter(normal_formatter)
        G_DISCORD_BOT_LOGGER.addHandler(file_handler)

def initialize_logger():
    setup_main_logger()
    setup_discord_bot_logger()







