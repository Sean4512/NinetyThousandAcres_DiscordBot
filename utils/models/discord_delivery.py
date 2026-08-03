# -*- coding: utf-8 -*-
"""
@File    : discord_delivery.py
@Time    : 2026/7/1 下午 01:18
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

__all__ = ["MessageDestination", "MessageVisibility", "Delivery", "Deliveries"]


class MessageDestination(str, Enum):
    DIRECT_MESSAGE = "direct_message"
    CHANNEL = "channel"
    THREAD = "thread"


class MessageVisibility(str, Enum):
    PRIVATE = "private"      # 僅 DM 使用
    EPHEMERAL = "ephemeral"  # 頻道/串中只有操作者看得到
    PUBLIC = "public"        # 頻道/串中所有人看得到


@dataclass(slots=True, frozen=True)
class Delivery:
    destination: MessageDestination
    visibility: MessageVisibility

    def __post_init__(self) -> None:
        if (
                self.destination is MessageDestination.DIRECT_MESSAGE
                and self.visibility is not MessageVisibility.PRIVATE
        ):
            raise ValueError(
                "DIRECT_MESSAGE 只能搭配 PRIVATE visibility。"
            )

        if (
                self.destination in
                {
                    MessageDestination.CHANNEL,
                    MessageDestination.THREAD,
                }
                and self.visibility is MessageVisibility.PRIVATE
        ):
            raise ValueError(
                "CHANNEL 或 THREAD 不可搭配 PRIVATE visibility，"
                "請使用 EPHEMERAL 或 PUBLIC。"
            )

    @property
    def is_direct_message(self) -> bool:
        return self.destination is MessageDestination.DIRECT_MESSAGE

    @property
    def interaction_ephemeral(self) -> bool:
        return not self.is_direct_message and self.visibility is MessageVisibility.EPHEMERAL


class Deliveries:
    DM = Delivery(MessageDestination.DIRECT_MESSAGE, MessageVisibility.PRIVATE)
    EPHEMERAL = Delivery(MessageDestination.CHANNEL, MessageVisibility.EPHEMERAL)
    PUBLIC = Delivery(MessageDestination.CHANNEL, MessageVisibility.PUBLIC)
    THREAD_PUBLIC = Delivery(MessageDestination.THREAD, MessageVisibility.PUBLIC)

