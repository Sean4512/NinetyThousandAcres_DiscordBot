# -*- coding: utf-8 -*-
"""
@File    : client.py
@Time    : 2026/4/11 上午 02:56
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord.ext import commands
from config.settings import get_discord_bot_settings

from utils.logger import get_discord_bot_logger
from config.load_discord_bot_extensions import load_enabled_extensions

__all__ = ["create_bot"]


class NinetyThousandAcresBot(commands.Bot):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    async def setup_hook(self) -> None:
        discord_bot_logger = get_discord_bot_logger()

        discord_bot_logger.info("load Discord bot extensions...")
        enabled_extensions = load_enabled_extensions()
        for extension_name in enabled_extensions:
            try:
                discord_bot_logger.info(f"Loaded extension {extension_name} ...")
                await self.load_extension(extension_name)
                discord_bot_logger.info(f"Loaded extension {extension_name} successfully.")
            except Exception as e:
                discord_bot_logger.error(f"Failed to load extension {extension_name}: {e}")
                raise ValueError(f"Failed to load extension {extension_name}: {e}") from e

        discord_bot_settings = get_discord_bot_settings()
        # 只同步到測試伺服器，更新比較快
        if discord_bot_settings.SYNCED_COMMAND:
            if discord_bot_settings.SYNCED_COMMAND_FOR_DEBUG:
                guild = discord.Object(id=discord_bot_settings.GUILD_ID_FOR_DEBUG)
                synced = await self.tree.sync(guild=guild)
                discord_bot_logger.info(
                    f"Synced {len(synced)} command(s) to guild {discord_bot_settings.GUILD_ID_FOR_DEBUG}.")

            else:
                synced = await self.tree.sync()
                discord_bot_logger.info(
                    f"Synced {len(synced)} command(s) to all servers")
            discord_bot_logger.info("Guild sync completed: %s", [cmd.name for cmd in synced])

        else:
            discord_bot_logger = get_discord_bot_logger()
            discord_bot_logger.warning(f"SYNCED_COMMAND not set, skip guild sync")


    async def on_ready(self):
        discord_bot_logger = get_discord_bot_logger()
        discord_bot_logger.info(f"Logged in as {self.user} (ID: {self.user.id})")


def create_bot() -> commands.Bot:
    discord_bot_settings = get_discord_bot_settings()
    intents = discord.Intents.default()

    bot = NinetyThousandAcresBot(
        command_prefix=discord_bot_settings.COMMAND_PREFIX,
        intents=intents,
    )

    return bot


