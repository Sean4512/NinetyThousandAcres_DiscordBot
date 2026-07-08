# -*- coding: utf-8 -*-
"""
@File    : main.py
@Time    : 2026/4/11 上午 02:59
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import asyncio
from discord.ext import commands
from utils.logger import get_main_logger, create_discord_bot_logger
from bot.client import create_bot

from config.settings import get_nta_settings, get_logger_settings, get_discord_bot_settings, get_database_settings
from config.check_settings import check_logger_settings
from database.init_db import init_db

async def run_discord_bot(bot: commands.Bot):
    discord_bot_settings = get_discord_bot_settings()
    await bot.start(discord_bot_settings.BOT_TOKEN)

async def main():

    main_logger = get_main_logger()
    main_logger.info("Starting app...")

    discord_bot_settings = get_discord_bot_settings()
    main_logger.info(f"{get_logger_settings()}") # Logger settings:
    main_logger.info(f"{get_nta_settings()}") # NTA settings:
    main_logger.info(f"{discord_bot_settings}") # Discord bot settings:
    main_logger.info(f"{get_database_settings()}") # Database bot settings:

    try:
        if not discord_bot_settings.BOT_TOKEN:
            raise ValueError("DISCORD_BOT_TOKEN 未設定，請檢查 .env")

        check_logger_settings()
        main_logger.info("The logger configuration is correct.")

        create_discord_bot_logger()
        main_logger.info("The bot configuration is correct.")

        main_logger.info("Initializing database...")
        init_db()
        main_logger.info("The Database configuration is correct.")

    except Exception as e:
        main_logger.error(f"程式啟動失敗: {e}")
        raise

    bot = None
    try:
        main_logger.info("Creating DiscordBot...")
        bot = create_bot()
        main_logger.info("The Discord Bot creation is correct.")

        main_logger.info("Starting Discord Bot...")
        await run_discord_bot(bot)


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

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger = get_main_logger()
        logger.info("Received Ctrl+C, program terminated.")
