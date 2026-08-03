# -*- coding: utf-8 -*-
"""
@File    : senders.py
@Time    : 2026/7/1 下午 01:22
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import discord
from discord.utils import MISSING
from utils.models.discord_delivery import  Delivery, MessageDestination
from utils.exceptions.discord_exceptions import (
    GuildRequiredError, GuildThreadRequiredError, GuildChannelRequiredError,
    ThreadChannelUnsupportedError)

__all__ = [
    "reply_to_interaction",
    "dispatch_message",
]


def _validate_destination(interaction: discord.Interaction, delivery: Delivery) -> None:
    destination = delivery.destination
    channel = interaction.channel

    if destination is MessageDestination.DIRECT_MESSAGE:
        return

    if interaction.guild is None:
        raise GuildRequiredError()

    if destination is MessageDestination.THREAD:
        if not isinstance(channel, discord.Thread):
            raise GuildThreadRequiredError()
        return

    if destination is MessageDestination.CHANNEL:
        if isinstance(channel, discord.Thread):
            raise ThreadChannelUnsupportedError()
        if not isinstance(channel, (discord.TextChannel, discord.VoiceChannel, discord.StageChannel)):
            raise GuildChannelRequiredError()

async def reply_to_interaction(
    interaction: discord.Interaction,
    *,
    content: str | None = None,
    embed: discord.Embed = MISSING,
    view: discord.ui.View = MISSING,
    ephemeral: bool = True,
) -> discord.Message:
    """interaction 專用：自動處理 尚未回應 vs 已回應。"""
    if interaction.response.is_done():
        return await interaction.followup.send(
            content=content, embed=embed, view=view,
            ephemeral=ephemeral, wait=True,
        )
    await interaction.response.send_message(
        content=content, embed=embed, view=view, ephemeral=ephemeral,
    )
    return await interaction.original_response()

async def dispatch_message(
    interaction: discord.Interaction,
    delivery: Delivery,
    *,
    user: discord.User | discord.Member,
    content: str | None = None,
    embed: discord.Embed | None = None,
    view: discord.ui.View | None = None,
) -> discord.Message:
    """依 Delivery 路由。等同你現在的 send_questionnaire_message，但抽成通用。"""
    if delivery.is_direct_message:
        return await user.send(content=content, embed=embed, view=view)

    _validate_destination(interaction, delivery)  # 你 flow 裡那段 validate 搬過來
    return await reply_to_interaction(
        interaction,
        content=content, embed=embed, view=view,
        ephemeral=delivery.interaction_ephemeral,
    )
