# -*- coding: utf-8 -*-
"""
@File    : questionnaire_runner.py
@Time    : 2026/8/2 下午 07:31
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from utils.models.questionnaire import Questionnaire, QuestionnaireResult


ContextT = TypeVar("ContextT")


class QuestionnaireRunner(ABC, Generic[ContextT]):
    """把一份 Questionnaire 呈現給使用者、並收集答案的抽象基底。

    這一層只定義「約定」，不碰任何具體介面：
        收一份 Questionnaire（題目）
        → 用某種介面問使用者
        → 回一份 QuestionnaireResult（答案）

    「用哪一種介面問」由子類別決定：
        DiscordQuestionnaireRunner     -> 用 Discord Modal
        GoogleFormQuestionnaireRunner  -> 用 Google 表單（未來）
    """

    @abstractmethod
    async def run(
        self,
        questionnaire: Questionnaire,
        context: ContextT,
        *,
        initial_answers: dict[str, Any] | None = None,
    ) -> QuestionnaireResult:
        """向使用者呈現 `questionnaire` 並回傳作答結果。

        子類別必須實作：
            1. 讀 questionnaire.fields / steps 取得題目
            2. 用 initial_answers 當作各欄位的預設值（供「修改既有答案」使用）
            3. 透過自己的介面（context）詢問使用者
            4. 回傳 QuestionnaireResult(answers=..., completed=...)

        Args:
            questionnaire: 要問的題目定義（與介面無關）。
            context: 該介面執行所需的情境，型別由子類別指定
                     （例如 Discord 版就是 discord.Interaction）。
            initial_answers: 各欄位的預填答案（key -> value）。使用者若只是要
                     修改，就不必整份重填；None 代表全部空白。
        """
        raise NotImplementedError
