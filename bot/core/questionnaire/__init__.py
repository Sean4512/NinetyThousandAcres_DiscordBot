# -*- coding: utf-8 -*-
"""
@File    : __init__.py
@Time    : 2026/8/2 下午 02:10
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : Discord 介面的問卷執行器（對外只暴露 DiscordQuestionnaireRunner）。
"""

from bot.core.questionnaire.runner import DiscordQuestionnaireRunner

__all__ = ["DiscordQuestionnaireRunner"]
