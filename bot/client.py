# -*- coding: utf-8 -*-
"""
@File    : client.py
@Time    : 2026/6/30 下午 06:54
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from pathlib import Path
import yaml
import discord
from discord.ext import commands

from config.settings import get_discord_bot_settings
from utils.logger import get_discord_bot_logger


def load_enabled_extensions() -> list[str]:

    discord_bot_settings = get_discord_bot_settings()
    config_path = Path(discord_bot_settings.EXTENSIONS_YAML_PATH)
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        raise ValueError(f"讀取Discord bot的extensions yaml時發生錯誤[{config_path}]: {e}") from e

    try:
        dc_commands = data.get("commands", [])
        enabled_extensions = []
        for item in dc_commands:
            if item.get("enabled", False):
                enabled_extensions.append(item["name"])
    except Exception as e:
        raise ValueError(f"讀取Discord bot的extensions時發生錯誤: {e}") from e

    return enabled_extensions


class NinetyThousandAcresBot(commands.Bot):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.logger = get_discord_bot_logger()

    async def setup_hook(self) -> None:
        self.logger.info("load Discord bot extensions...")
        enabled_extensions = load_enabled_extensions()
        for extension_name in enabled_extensions:
            try:
                self.logger.info(f"Loaded extension {extension_name} ...")
                await self.load_extension(extension_name)
                self.logger.info(f"Loaded extension {extension_name} successfully.")
            except Exception as e:
                self.logger.error(f"Failed to load extension {extension_name}: {e}")
                raise ValueError(f"Failed to load extension {extension_name}: {e}") from e

        discord_bot_settings = get_discord_bot_settings()
        if discord_bot_settings.SYNC_COMMANDS:
            synced = await self.tree.sync()
            self.logger.info(f"Synced {len(synced)} command(s) to all servers")
            self.logger.info("Guild sync completed: %s", [cmd.name for cmd in synced])
        else:
            self.logger.warning(f"SYNCED_COMMAND not set, skip guild sync")

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

def create_bot() -> commands.Bot:
    discord_bot_settings = get_discord_bot_settings()
    intents = discord.Intents.default()

    bot = NinetyThousandAcresBot(
        command_prefix=discord_bot_settings.COMMAND_PREFIX,
        intents=intents,
    )

    return bot

