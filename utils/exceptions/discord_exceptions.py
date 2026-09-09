# -*- coding: utf-8 -*-
"""
@File    : discord_exceptions.py
@Time    : 2026/7/1 上午 01:55
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from utils.exceptions._base import BaseError


class DebugError(BaseError):
    _message: str = "此功能尚未開放。"
    def __init__(self, message: str = ""):
        self._message = self._message + (f"\n{message}" if message else "")
        super().__init__(self._message)

class InternalError(BaseError):
    _message = "伺服器內部出現異常，請稍後再試或聯繫Bot開發者。"

class AdminPermissionError(BaseError):
    _message = "你沒有權限使用這個指令"

class FlowOwnerMismatchError(BaseError):
    _message = "這不是你的操作流程。"

class GuildRequiredError(BaseError):
    _message = "此指令只能在伺服器內使用。"

class GuildThreadRequiredError(BaseError):
    _message = "此操作只能在討論串中執行。"

class GuildChannelRequiredError(BaseError):
    _message = "此操作必須在伺服器頻道中執行。"

class ThreadChannelUnsupportedError(BaseError):
    _message = "此操作不能在討論串中執行。"

class GuildInitializedFailedError(BaseError):
    _message = "伺服器初始化失敗。"

class GuildNotInitializedError(BaseError):
    _message = "此伺服器尚未初始化，請管理員先完成伺服器設定(/setup)。"

class MatchSignupForumThreadRequiredError(BaseError):
    _message: str = "❌ 請在報名論壇內的報名貼文中執行此指令。"


G_DISCORD_EXCEPTIONS = [
    DebugError,
    InternalError,
    AdminPermissionError,
    FlowOwnerMismatchError,
    GuildRequiredError,
    GuildThreadRequiredError,
    GuildChannelRequiredError,
    ThreadChannelUnsupportedError,

]


if __name__ == "__main__":
    for error in G_DISCORD_EXCEPTIONS:
        print(error().message)

