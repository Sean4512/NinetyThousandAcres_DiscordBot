# -*- coding: utf-8 -*-
"""
@File    : guild_setup.py
@Time    : 2026/7/5 下午 03:46
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.core import BaseCog
from services import GuildService, GuildConfigKeys

from utils.logger import get_discord_bot_logger
from utils.exceptions.discord_exceptions import GuildRequiredError, GuildInitializedFailedError, DebugError


class GuildSetupCog(BaseCog):

    @app_commands.command(name="setup", description="初始化機器人，每一個伺服器都需要設定一次")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def setup(
        self,
        interaction: discord.Interaction,
        admin_role: discord.Role,
        category: discord.CategoryChannel,
        registration_forum: discord.ForumChannel | None = None,
    ):
        guild = interaction.guild
        if guild is None:
            raise GuildRequiredError()

        created_registration_forum_by_bot = False
        if registration_forum is None:
            #  在群組中建立報名討論串
            try:
                registration_forum = await self._create_registration_forum(
                    guild,
                    name="報名區",
                    category=category,
                    reason="初始化九萬畝報名區(ForumChannel)",
                )
                created_registration_forum_by_bot = True
            except discord.Forbidden as error:
                raise GuildInitializedFailedError(
                    "Bot 缺少建立報名區所需的權限，請確認 Bot 是否具有「管理頻道」權限。") from error

            except Exception as error:
                raise GuildInitializedFailedError() from error

        try:
            GuildService.initialize_guild(
                guild.id,
                {
                    GuildConfigKeys.ADMIN_ROLE_ID: str(admin_role.id),
                    GuildConfigKeys.CATEGORY_ID: str(category.id),
                    GuildConfigKeys.REGISTRATION_FORUM_ID: (
                        str(registration_forum.id) if registration_forum is not None else None
                    ),
                },
            )
        except Exception:
            if created_registration_forum_by_bot and registration_forum is not None:
                #  如果是系統建立的 報名串 那麼將他刪除
                await registration_forum.delete(
                    reason="初始化失敗，自動刪除本次建立的報名 ForumChannel",
                )
            raise

        log_message = (f"Guild setup executed. "
                       f"guild_id={guild.id}, guild_name={guild.name}, "
                       f"admin_role_id={admin_role.id}, category_id={category.id}, "
                       f"registration_forum_id={registration_forum.id} ")
        self.logger.info(log_message)

        if created_registration_forum_by_bot:
            reply_message = f"✅ 初始化完成。已為你建立報名區：{registration_forum.mention}"
        else:
            reply_message = f"✅ 初始化完成。報名區：{registration_forum.mention}"
        await self.safe_reply(interaction, reply_message)

    @staticmethod
    async def _create_registration_forum(
        guild: discord.Guild,
        **kwargs
    ):
        registration_forum = await guild.create_forum(**kwargs)
        return registration_forum

    @app_commands.command(name="update_registration_forum", description="更新機器人的資料")
    @app_commands.guild_only()
    async def update_registration_forum(
        self,
        interaction: discord.Interaction,
    ):
        raise DebugError()



async def setup(bot: commands.Bot):
    discord_bot_logger = get_discord_bot_logger()
    discord_bot_logger.debug("loading Setup Cog...")
    await bot.add_cog(GuildSetupCog(bot))

