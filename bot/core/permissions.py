# -*- coding: utf-8 -*-
"""
@File    : permissions.py
@Time    : 2026/7/25 上午 01:55
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord import app_commands

from services.guild_service import GuildService, GuildConfigKeys
from utils.exceptions.discord_exceptions import GuildNotInitializedError


async def ensure_admin_interaction(interaction: discord.Interaction) -> bool:

    admin_role_id = GuildService.get_config_value(interaction.guild.id, GuildConfigKeys.ADMIN_ROLE_ID)
    if admin_role_id is None:
        raise GuildNotInitializedError()

    return any(str(r.id) == admin_role_id for r in interaction.user.roles)

def is_guild_admin():
    async def predicate(interaction: discord.Interaction) -> bool:
        return await ensure_admin_interaction(interaction)
    return app_commands.check(predicate)