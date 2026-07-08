# -*- coding: utf-8 -*-
"""
@File    : load_discord_bot_extensions.py
@Time    : 2026/4/13 下午 04:29
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from pathlib import Path
import yaml

from .settings import get_discord_bot_settings

__all__ = ["load_enabled_extensions"]

def load_enabled_extensions() -> list[str]:
    discord_bot_settings = get_discord_bot_settings()

    config_path = Path(discord_bot_settings.EXTENSIONS_YAML_PATH)
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        raise ValueError(f"讀取Discord bot的extensions yaml時發生錯誤[{config_path}]: {e}") from e

    try:
        commands = data.get("commands", [])
        enabled_extensions = []
        for item in commands:
            if item.get("enabled", False):
                enabled_extensions.append(item["name"])
    except Exception as e:
        raise ValueError(f"讀取Discord bot的extensions時發生錯誤: {e}") from e

    return enabled_extensions
