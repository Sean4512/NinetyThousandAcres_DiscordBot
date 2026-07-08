# -*- coding: utf-8 -*-
"""
@File    : utils.py
@Time    : 2026/5/10 上午 03:30
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations

__all__ = ["send_interaction_message", "InteractionResponderMixin", "ensure_allowed_user"]

import discord

from utils.logger import get_discord_bot_logger


DEFAULT_INTERACTION_ERROR_MESSAGE = "伺服器內部出現異常，請稍後再試或聯繫 Bot 開發者。"


async def send_interaction_message(
    interaction: discord.Interaction,
    message: str = DEFAULT_INTERACTION_ERROR_MESSAGE,
    *,
    ephemeral: bool = True,
) -> None:
    """
    安全回覆 Discord interaction。

    如果 interaction 尚未回應：
        使用 interaction.response.send_message()

    如果 interaction 已經回應：
        使用 interaction.followup.send()
    """
    if interaction.response.is_done():
        await interaction.followup.send(
            content=message,
            ephemeral=ephemeral,
        )
        return

    await interaction.response.send_message(
        content=message,
        ephemeral=ephemeral,
    )


class InteractionResponderMixin:
    """
    提供安全回覆 Discord interaction 的 mixin。
    """

    async def send_interaction_message(
        self,
        interaction: discord.Interaction,
        message: str = DEFAULT_INTERACTION_ERROR_MESSAGE,
        *,
        ephemeral: bool = True,
    ) -> None:
        logger = getattr(self, "logger", get_discord_bot_logger())

        try:
            await send_interaction_message(
                interaction=interaction,
                message=message,
                ephemeral=ephemeral,
            )

        except discord.NotFound:
            logger.exception(
                "%s.send_interaction_message failed: interaction not found or expired. "
                "user_id=%s, user_name=%s",
                self.__class__.__name__,
                getattr(interaction.user, "id", None),
                getattr(interaction.user, "name", None),
            )

        except discord.Forbidden:
            logger.exception(
                "%s.send_interaction_message failed: missing permission. "
                "user_id=%s, user_name=%s",
                self.__class__.__name__,
                getattr(interaction.user, "id", None),
                getattr(interaction.user, "name", None),
            )

        except discord.HTTPException:
            logger.exception(
                "%s.send_interaction_message failed: Discord HTTP error. "
                "user_id=%s, user_name=%s",
                self.__class__.__name__,
                getattr(interaction.user, "id", None),
                getattr(interaction.user, "name", None),
            )


async def ensure_allowed_user(
    interaction: discord.Interaction,
    allowed_user_id: int,
    *,
    message: str = "這不是你的註冊流程。",
    ephemeral: bool = True,
) -> bool:
    """
    確認目前 interaction.user 是否為允許操作的使用者。

    Returns
    -------
    bool
        True  = 是本人，可以繼續流程
        False = 不是本人，已送出提示訊息，應該中斷流程
    """
    if interaction.user.id == allowed_user_id:
        return True

    await send_interaction_message(
        interaction=interaction,
        message=message,
        ephemeral=ephemeral,
    )
    return False
