# -*- coding: utf-8 -*-
"""
@File    : main.py
@Time    : 2026/6/30 下午 05:09
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import asyncio

from config import settings

from config.settings import (
    initialize_settings,get_nta_settings, get_logger_settings, get_discord_bot_settings, get_database_settings
)
from config.questionnaire_settings import setup_all_questionnaires
from config.check_settings import check_logger_settings

from database.database import initialize_database

from bot.client import create_bot
from utils.logger import initialize_logger, get_main_logger



async def run_discord_bot():
    main_logger = get_main_logger()

    bot = None
    try:
        main_logger.info("Creating DiscordBot...")
        bot = create_bot()
        main_logger.info("The Discord Bot creation is correct.")

        main_logger.info("Starting Discord Bot...")
        await bot.start(get_discord_bot_settings().BOT_TOKEN)


    except asyncio.CancelledError:
        main_logger.warning("Discord Bot task was cancelled.")
        raise

    except Exception as e:
        main_logger.error(f"程式運行失敗: {e}")
        raise

    finally:
        if bot is not None:
            main_logger.info("Closing Discord Bot...")
            try:
                await bot.close()
            except Exception as close_error:
                main_logger.error(f"關閉 Discord Bot 時發生錯誤: {close_error}")
            else:
                main_logger.info("Discord Bot closed.")


def main():
    initialize_settings()
    initialize_logger()

    main_logger = get_main_logger()
    main_logger.info("Starting app...")

    discord_bot_settings = get_discord_bot_settings()
    main_logger.info(f"{get_logger_settings()}")  # Logger settings:
    main_logger.info(f"{get_nta_settings()}")  # NTA settings:
    main_logger.info(f"{discord_bot_settings}")  # Discord bot settings:
    main_logger.info(f"{get_database_settings()}")  # Database bot settings:

    try:
        if not discord_bot_settings.BOT_TOKEN:
            raise ValueError("DISCORD_BOT_TOKEN 未設定，請檢查 .env")

        check_logger_settings()
        main_logger.info("The logger configuration is correct.")

        main_logger.info("Initializing database...")
        initialize_database()
        main_logger.info("The Database configuration is correct.")

        main_logger.info("Initializing questionnaires...")
        setup_all_questionnaires()
        main_logger.info("The Questionnaires configuration is correct.")

    except Exception as e:
        main_logger.error(f"Program failed to start: {e}")
        raise



    try:
        asyncio.run(run_discord_bot())
    except KeyboardInterrupt:
        logger = get_main_logger()
        logger.info("Received Ctrl+C, program terminated.")


if __name__ == '__main__':
    main()
