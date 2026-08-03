# -*- coding: utf-8 -*-
"""
@File    : _base.py
@Time    : 2026/7/6 上午 01:37
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from discord import app_commands


class BaseError(app_commands.AppCommandError):
    _message: str = "BaseError"
    def __init__(self, message: str = ""):
        if message:
            self._message = message
        super().__init__(self.message)

    @property
    def message(self) -> str:
        return self._message
