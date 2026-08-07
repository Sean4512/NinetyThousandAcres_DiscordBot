# -*- coding: utf-8 -*-
"""
@File    : cog.py
@Time    : 2026/8/1 下午 09:28
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from typing import Optional
import discord
from discord import app_commands

from bot.core import BaseCog, DiscordQuestionnaireRunner
from bot.core.permissions import ensure_admin_interaction
from config.questionnaire_settings import get_match_signup_creation_questionnaire
from services.guild_service import GuildService, GuildConfigKeys
from services.match_signup.form_service import MatchSignupConfigKeys, MatchSignupFormService, MatchSignupThreadStatus
from utils.exceptions.discord_exceptions import GuildRequiredError, GuildNotInitializedError


class MatchSignupCreationGroup(app_commands.Group):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:

        guild = interaction.guild
        if guild is None:
            raise GuildRequiredError()

        if not GuildService.is_initialized(interaction.guild.id):
            raise GuildNotInitializedError()

        if not await ensure_admin_interaction(interaction):
            return False
        return True


async def get_registration_forum(
    guild: discord.Guild,
    registration_forum_id: str | int,
) -> Optional[discord.ForumChannel]:
    try:
        forum_id = int(registration_forum_id)
    except (TypeError, ValueError):
        return None

    channel = guild.get_channel(forum_id)

    if channel is None:
        try:
            # 快取不存在時，向 Discord API 查詢
            channel = await guild.fetch_channel(forum_id)

        except discord.NotFound:
            # 頻道不存在或已被刪除
            return None

        except discord.Forbidden:
            # Bot 沒有查看該頻道的權限
            return None

        except discord.HTTPException:
            # Discord API 呼叫失敗
            return None

        # 防止資料庫中的 ID 指向另一個伺服器的頻道
    if channel.guild.id != guild.id:
        return None

    if not isinstance(channel, discord.ForumChannel):
        return None

    return channel


class MatchSignupFormCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.questionnaire_runner = DiscordQuestionnaireRunner()

    match_signup = MatchSignupCreationGroup(
        name="match_signup_admin",
        description="管理員 建立戰爭報名的相關指令",
        guild_only=True,
    )

    @match_signup.command(name="create", description="幫指定玩家建立註冊資料")
    async def create_match(self, interaction: discord.Interaction):

        registration_forum_id = GuildService.get_config_value(interaction.guild.id, GuildConfigKeys.REGISTRATION_FORUM_ID)
        if registration_forum_id is None:
            raise GuildNotInitializedError()

        guild: discord.Guild = interaction.guild

        registration_forum = await get_registration_forum(guild, registration_forum_id)

        if registration_forum is None:
            raise GuildNotInitializedError()

        questionnaire = get_match_signup_creation_questionnaire()
        result = await self.questionnaire_runner.run(questionnaire, interaction)

        if not result.completed:
            return

        title = result.answers.get(MatchSignupConfigKeys.TITLE)
        content = result.answers.get(MatchSignupConfigKeys.CONTENT)
        if not isinstance(title, str):
            raise TypeError("title 必須是 str")
        elif not isinstance(content, str):
            raise TypeError("content 必須是 str")

        try:
            new_thread = await registration_forum.create_thread(
                name=title,
                content=(
                    f"{content}\n\n"
                    "請點擊下方按鈕完成報名。"
                ),
                # view=BaseView(),
                reason="Create match signup forum thread",
            )
        except Exception as e:
            raise

        thread: discord.Thread = new_thread.thread
        message: discord.Message = new_thread.message

        MatchSignupFormService.create(
            guild_id=guild.id,
            forum_id=registration_forum.id,
            thread_id=thread.id,
            message_id=message.id,
            status=MatchSignupThreadStatus.OPEN,
            title=title,
            content=content,
        )

        await self.safe_reply(
            interaction,
            message=f"{thread.mention}"
        )
        await interaction.user.send(
            content=f"{thread.mention}"
        )

    @match_signup.command(name="delete", description="刪除報名表")
    async def delete(
        self,
        interaction: discord.Interaction,
    ):
        guild: discord.Guild = interaction.guild
        registration_forum_id = GuildService.get_config_value(
            guild.id,
            GuildConfigKeys.REGISTRATION_FORUM_ID,
        )
        if registration_forum_id is None:
            raise GuildNotInitializedError()

        registration_forum = await get_registration_forum(
            guild,
            registration_forum_id,
        )
        if registration_forum is None:
            raise GuildNotInitializedError()

        thread = interaction.channel

        if not isinstance(thread, discord.Thread):
            await self.safe_reply(
                interaction,
                "❌ 請進入要刪除的報名貼文後再執行此指令。",
            )
            return

        if thread.guild.id != guild.id or thread.parent_id != registration_forum.id:
            await self.safe_reply(
                interaction,
                "❌ 只能刪除報名論壇內的討論串。",
            )
            return

        if not MatchSignupFormService.exists(guild.id, thread.id):
            await self.safe_reply(
                interaction,
                "❌ 此討論串不是由報名系統建立的報名表，無法刪除。",
            )
            return

        thread_name = thread.name
        await thread.delete(reason="Delete match signup forum thread")
        MatchSignupFormService.delete(guild.id, thread.id)

        # await self.safe_reply(
        #     interaction,
        #     f"✅ 已刪除報名表：{thread_name}",
        # )
        await interaction.user.send(f"✅ 已刪除報名表：{thread_name}")










