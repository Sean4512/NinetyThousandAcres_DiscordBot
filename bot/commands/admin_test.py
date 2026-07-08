# -*- coding: utf-8 -*-
"""
@File    : admin_test.py
@Time    : 2026/4/15 上午 01:39
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.core.base_cog import BaseCog
from services.auth_service import AuthService
from services.guild_service import GuildService
from utils.logger import get_discord_bot_logger

from utils.exceptions.discord_exceptions import AdminPermissionError, GuildNotInitializedError, GuildOnlyError


async def ensure_admin_interaction(interaction: discord.Interaction) -> bool:
    logger = get_discord_bot_logger()

    command_name = (
        interaction.command.qualified_name
        if interaction.command is not None
        else "unknown_command"
    )

    guild = interaction.guild
    if guild is None:
        logger.warning(
            "%s blocked: guild is None. user_id=%s, user_name=%s{%s}",
            command_name,
            interaction.user.id,
            interaction.user.name,
            interaction.user.global_name,
        )
        raise GuildOnlyError()

    if not isinstance(interaction.user, discord.Member):
        logger.warning(
            "%s blocked: user is not Member. guild_id=%s, guild_name=%s, user_id=%s, user_name=%s{%s}",
            command_name,
            guild.id,
            guild.name,
            interaction.user.id,
            interaction.user.name,
            interaction.user.global_name,
        )
        raise AdminPermissionError("無法取得你的伺服器身分組資訊。")

    guild_id = str(guild.id)
    guild_is_exists = GuildService.is_exists(guild_id)
    if not guild_is_exists:
        raise GuildNotInitializedError()

    guild_config = GuildService.get_guild_config_by_guild_id(
        guild_id
    )

    state: bool
    user_role_ids = [str(role.id) for role in interaction.user.roles]

    state = AuthService.has_admin_role(
        guild_config=guild_config,
        user_role_ids=user_role_ids,
    )

    if not state:
        logger.warning(
            "%s blocked: missing admin role. guild_id=%s, guild_name=%s, user_id=%s, user_name=%s{%s}",
            command_name,
            guild.id,
            guild.name,
            interaction.user.id,
            interaction.user.name,
            interaction.user.global_name,
        )
        raise AdminPermissionError()

    logger.info(
        "%s authorized. guild_id=%s, guild_name=%s, user_id=%s, user_name=%s{%s}",
        command_name,
        guild.id,
        guild.name,
        interaction.user.id,
        interaction.user.name,
        interaction.user.global_name,
    )

    return True

def admin_required():
    async def predicate(interaction: discord.Interaction) -> bool:
        return await ensure_admin_interaction(interaction)
    return app_commands.check(predicate)


class AdminTestCog(BaseCog):

    @app_commands.command(name="admin_test", description="測試只有特定身分組可以執行的指令")
    @app_commands.guild_only()
    @admin_required()
    async def admin_test(self, interaction: discord.Interaction):

        await self.send_interaction_message(
            interaction,
            "你有對應的身分組權限。"
        )

        guild = interaction.guild
        if guild is None:
            raise GuildOnlyError()

        self.logger.info(
            "admin_test executed by user_id=%s guild_id=%s",
            interaction.user.id,
            guild.id
        )


async def setup(bot: commands.Bot):
    discord_bot_logger = get_discord_bot_logger()
    discord_bot_logger.debug("loading AdminTest Cog...")
    await bot.add_cog(AdminTestCog(bot))