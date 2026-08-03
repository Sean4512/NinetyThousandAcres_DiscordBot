# -*- coding: utf-8 -*-
"""
@File    : service_exceptions.py
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : Service（商業邏輯）層的 domain 例外。

這些例外繼承自 discord_exceptions.BaseError，因此帶有一段給使用者看的 message，
並會被 cog 的 cog_app_command_error -> handle_app_error 統一攔截後回覆。
"""

from utils.exceptions._base import BaseError


# ---------- Guild ----------

class GuildAlreadySetupError(BaseError):
    _message: str = "此伺服器已經初始化過了，若要重新設定請先移除舊設定。"


class GuildNotSetupError(BaseError):
    _message: str = "此伺服器尚未初始化，請先使用 /setup 進行設定。"


class PlayerAlreadyRegisteredError(BaseError):
    _message: str = "已經註冊過了，若要修改資料請使用更新指令。"

class PlayerNotRegisteredError(BaseError):
    _message: str = "尚未註冊，請先使用 /player_registration 註冊。"


G_SERVICE_EXCEPTIONS = [
    GuildAlreadySetupError,
    GuildNotSetupError,
    PlayerAlreadyRegisteredError,
    PlayerNotRegisteredError
]


if __name__ == "__main__":
    for error in G_SERVICE_EXCEPTIONS:
        print(error().message)
