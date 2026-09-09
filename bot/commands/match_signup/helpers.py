# -*- coding: utf-8 -*-
"""
@File    : helpers.py
@Time    : 2026/8/7 下午 11:49
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from typing import Optional

import discord

from utils.exceptions.discord_exceptions import MatchSignupForumThreadRequiredError


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

def ensure_thread_in_forum(guild: discord.Guild, forum: discord.ForumChannel, thread: discord.Thread):

    if not isinstance(thread, discord.Thread):
        raise MatchSignupForumThreadRequiredError()
    if thread.guild.id != guild.id or thread.parent_id != forum.id:
        raise MatchSignupForumThreadRequiredError()

