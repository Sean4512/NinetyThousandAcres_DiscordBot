# -*- coding: utf-8 -*-
"""
@File    : discord_exceptions.py
@Time    : 2026/5/8 上午 03:48
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from discord import app_commands

# __all__ = ["DebugError", "DISCORD_EXCEPTIONS", "AdminPermissionError", "PlayerInitializationError", "InternalError", "GuildNotInitializedError", "PlayerAlreadyRegisteredError", "GuildOnlyError", "PlayerNoRegisteredError"]

class DebugError(app_commands.CheckFailure):
    def __init__(self, _message: str | None = None):
        _message = str(_message)
        self.message = "此功能尚未開放。"
        self.message += f"\n{_message}" if _message is not None else ""
        super().__init__(self.message)

class InternalError(app_commands.CheckFailure):
    def __init__(self, message: str | None = None):
        self.message = message or "伺服器內部出現異常，請稍後再試或聯繫Bot開發者。"
        super().__init__(self.message)

class AdminPermissionError(app_commands.CheckFailure):
    def __init__(self, message: str | None = None):
        self.message = message or "你沒有權限使用這個指令，或此伺服器尚未初始化。"
        super().__init__(self.message)

class GuildOnlyError(app_commands.CheckFailure):
    def __init__(self, message: str | None = None):
        super().__init__(message or "此指令只能在伺服器內使用。")

class GuildNotInitializedError(app_commands.CheckFailure):
    def __init__(self, message: str | None = None):
        self.message = message or "此伺服器尚未初始化，請管理員先完成伺服器設定(/setup)。"
        super().__init__(self.message)

class GuildInitializedFailedError(app_commands.CheckFailure):
    def __init__(self, message: str | None = None):
        self.message = message or "伺服器初始化失敗。"
        super().__init__(self.message)

class PlayerInitializationError(app_commands.CheckFailure):
    def __init__(self, message: str | None = None):
        self.message = message or "你在此伺服器尚未初始化完成，請先執行 /player_register。"
        super().__init__(self.message)

class PlayerAlreadyRegisteredError(app_commands.CheckFailure):
    def __init__(self, message: str | None = None):
        self.message = message or "你已經註冊過了。"
        super().__init__(self.message)

class PlayerNoRegisteredError(app_commands.CheckFailure):
    def __init__(self, message: str | None = None):
        self.message = message or "玩家尚未註冊過了。"
        super().__init__(self.message)

class ParameterError(app_commands.CheckFailure):
    def __init__(self, message: str | None = None):
        self.message = message or "玩家尚未註冊過了。"
        super().__init__(self.message)

class InvalidInteractionContextError(app_commands.CheckFailure):
    def __init__(self, message: str | None = None):
        self.message = message or "交互錯誤。"
        super().__init__(self.message)

DISCORD_EXCEPTIONS = (
    DebugError,
    InternalError,
    InvalidInteractionContextError,
    GuildNotInitializedError,
    GuildInitializedFailedError,
    AdminPermissionError,
    PlayerInitializationError,
    PlayerAlreadyRegisteredError,
    PlayerNoRegisteredError,
    ParameterError
)





