# -*- coding: utf-8 -*-
"""
@File    : guild_setup.py
@Time    : 2026/4/14 上午 12:21
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.core.base_cog import BaseCog
from services.guild_service import GuildService
from utils.logger import get_discord_bot_logger
from utils.exceptions.discord_exceptions import GuildOnlyError, GuildInitializedFailedError

class SetupCog(BaseCog):

    @app_commands.command(name="setup", description="初始化機器人，每一個伺服器都需要設定一次")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def setup(
            self,
            interaction: discord.Interaction,
            admin_role: discord.Role,
            category: discord.CategoryChannel,
            registration_forum:discord.ForumChannel | None = None,
    ):
        guild = interaction.guild
        if guild is None:
            raise GuildOnlyError()

        success: bool
        message: str
        guild_id: str = str(guild.id)
        created_registration_forum_by_bot = False

        success, message = GuildService.insert_guild_profile(guild_id)
        if not success:
            await self.send_interaction_message(interaction, message)
            raise GuildInitializedFailedError()

        try:
            if registration_forum is None:
                registration_forum = await guild.create_forum(
                    name="報名區",
                    category=category,
                    reason="初始化九萬畝報名區(ForumChannel)",
                )
                created_registration_forum_by_bot = True
        except discord.Forbidden as error:
            raise GuildInitializedFailedError(
                "Bot 缺少建立報名區所需的權限，請確認 Bot 是否具有「管理頻道」權限。"
            ) from error


        try:
            configs: dict[str, str] = {
                "admin_role_id": str(admin_role.id),
                "category_id": str(category.id),
                "registration_forum_id": str(registration_forum.id)
            }
            success, message = GuildService.upsert_guild_config(
                guild_id=guild_id,
                configs=configs
            )
            if not success:
                await self.send_interaction_message(interaction, message)
                raise GuildInitializedFailedError()

            await self.send_interaction_message(interaction, message)
            self.logger.info(
                "Guild setup executed. guild_id=%s guild_name=%s success=%s admin_role_id=%s category_id=%s registration_forum_id=%s",
                guild.id,
                guild.name,
                success,
                admin_role.id,
                category.id,
                registration_forum.id,
            )

        except Exception:

            if created_registration_forum_by_bot and registration_forum is not None:
                try:
                    await registration_forum.delete(
                        reason="初始化失敗，自動刪除本次建立的報名 ForumChannel",
                    )
                except discord.HTTPException:
                    self.logger.exception(
                        "Failed to delete auto-created registration forum after setup failure."
                        f" guild_id={guild_id}, forum_id={registration_forum.id}"
                    )
            raise

        return

async def setup(bot: commands.Bot):
    discord_bot_logger = get_discord_bot_logger()
    discord_bot_logger.debug("loading Setup Cog...")
    await bot.add_cog(SetupCog(bot))


