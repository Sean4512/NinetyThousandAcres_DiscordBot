# -*- coding: utf-8 -*-
"""
@File    : check_settings.py
@Time    : 2026/6/30 下午 05:38
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from config import settings


def check_logger_settings():
    logger_levels = ["CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET"]
    bot_level = settings.get_logger_settings().BOT_LEVEL
    if bot_level not in logger_levels:
        raise ValueError(
            f"NINETY_THOUSAND_ACRES_BOT_LOG_LEVEL 設定錯誤：{bot_level}。"
            f"允許的值為：{', '.join(logger_levels)}"
        )
