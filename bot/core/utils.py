# -*- coding: utf-8 -*-
"""
@File    : utils.py
@Time    : 2026/7/1 下午 01:02
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations

import discord
from discord import app_commands

from bot.core.senders import reply_to_interaction

from utils.logger import get_discord_bot_logger
from utils.exceptions.discord_exceptions import InternalError, GuildRequiredError, BaseError

G_DEFAULT_INTERACTION_ERROR_MESSAGE = str(InternalError())


class InteractionResponderMixin:
    async def safe_reply(self, interaction, message=G_DEFAULT_INTERACTION_ERROR_MESSAGE, *, ephemeral=True) -> None:
        logger = getattr(self, "logger", get_discord_bot_logger())
        try:
            await reply_to_interaction(interaction, content=message, ephemeral=ephemeral)
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            logger.exception("safe_reply failed. user_id=%s",
                             getattr(interaction.user, "id", None))

    async def handle_app_error(self, interaction, error) -> None:
        original = getattr(error, "original", error)
        logger = getattr(self, "logger", get_discord_bot_logger())

        # 專案內所有帶使用者訊息的 domain 例外（discord 守衛 + service 商業例外）
        # 皆繼承 BaseError，統一以其 message 回覆。
        if isinstance(original, BaseError):
            await self.safe_reply(interaction, str(original))
            return
        if isinstance(original, discord.Forbidden):
            await self.safe_reply(interaction, "❌ 無法私訊你，請確認你有開啟伺服器成員私訊。")
            return
        if isinstance(original, app_commands.NoPrivateMessage):
            logger.warning("guild is None. user=%s", interaction.user.id)
            await self.safe_reply(interaction, str(GuildRequiredError()))
            return
        if isinstance(error, app_commands.CheckFailure):
            await self.safe_reply(interaction, "你沒有權限使用這個指令。")
            return

        logger.exception("Unhandled app command error. user_id=%s", interaction.user.id, exc_info=error)
        await self.safe_reply(interaction, InternalError().message)
        return

async def ensure_owner(
    interaction: discord.Interaction,
    allowed_user_id: int,
) -> bool:
    """
    確認目前 interaction.user 是否為允許操作的使用者
    :param interaction:
    :param allowed_user_id:
    :return: True(是本人, 可以繼續流程) or False(不是本人, 應該中斷流程)
    """
    if interaction.user.id == allowed_user_id:
        return True

    return False
