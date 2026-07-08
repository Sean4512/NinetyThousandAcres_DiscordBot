# -*- coding: utf-8 -*-
"""
@File    : logger.py
@Time    : 2026/4/11 下午 08:54
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import os
from config.settings import get_logger_settings
import logging

__all__ = ["create_discord_bot_logger", "get_discord_bot_logger", "get_main_logger"]

g_discord_bot_logger: logging.Logger | None = None

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

    # ANSI_color_sumary
    # https://gist.github.com/ThomasLau/3f2461188b7def566512
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

logger_settings = get_logger_settings()
# 確保log存入指定資料夾
if not os.path.isdir(logger_settings.DIRECTORY):
    os.makedirs(logger_settings.DIRECTORY, exist_ok=True)

# 避免資料夾建立失敗
if not os.path.isdir(logger_settings.DIRECTORY):
    raise ValueError("Logger directory not initialized")


# Main log
main_log_file = "main.log"
g_main_logger: logging.Logger = logging.getLogger("main")
if g_main_logger is None:
    raise ValueError("Logger not initialized")
g_main_logger.setLevel(logging.INFO)

# 避免重複加入 handler
if not g_main_logger.handlers:
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
    g_main_logger.addHandler(console_handler)

    # 輸出到檔案
    file_handler = logging.FileHandler(
        os.path.join(logger_settings.DIRECTORY, main_log_file),
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(normal_formatter)
    g_main_logger.addHandler(file_handler)


def get_main_logger() -> logging.Logger:
    global g_main_logger

    if g_main_logger is None:
        raise ValueError("Main logger not initialized")

    return g_main_logger

# 輸出有關 Discord bot 全部的資訊
def create_discord_bot_logger():
    global g_discord_bot_logger

    bot_log_file = "bot.log"
    g_discord_bot_logger = logging.getLogger("discord_bot")
    g_discord_bot_logger.setLevel(logger_name_to_level(logger_settings.BOT_LEVEL))

    # 避免重複加入 handler
    if not g_discord_bot_logger.handlers:
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
        g_discord_bot_logger.addHandler(console_handler)

        # 輸出到檔案
        file_handler = logging.FileHandler(
            os.path.join(logger_settings.DIRECTORY, bot_log_file),
            encoding="utf-8"
        )
        file_handler.setLevel(logger_name_to_level(logger_settings.BOT_LEVEL))
        file_handler.setFormatter(normal_formatter)
        g_discord_bot_logger.addHandler(file_handler)

    if g_discord_bot_logger is None:
        raise ValueError("Discord bot logger not initialized")

def get_discord_bot_logger() -> logging.Logger:
    global g_discord_bot_logger

    if g_discord_bot_logger is None:
        raise ValueError("Discord bot logger not initialized")

    return g_discord_bot_logger


