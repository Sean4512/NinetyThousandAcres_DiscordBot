# -*- coding: utf-8 -*-
"""
@File    : check_settings.py
@Time    : 2026/4/12 上午 11:22
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""


from . import settings





def check_logger_settings():
    pass

    logger_levels = ["CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET"]
    bot_level = settings.g_logger_settings.BOT_LEVEL
    if bot_level not in logger_levels:
        raise ValueError(
            f"NINETY_THOUSAND_ACRES_BOT_LOG_LEVEL 設定錯誤：{bot_level}。"
            f"允許的值為：{', '.join(logger_levels)}"
        )




