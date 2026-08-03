# -*- coding: utf-8 -*-
"""
@File    : questionnaire.py
@Time    : 2026/7/1 上午 01:16
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from utils.models.discord_delivery import *

__all__ = [
    "QuestionValidatorType",
    "QuestionComponentType",
    "QuestionField",
    "QuestionStep",
    "Questionnaire",
    "QuestionnaireResult",
]


class QuestionValidatorType(str, Enum):
    NONE = "none"
    INT = "int"
    YES_NO = "yes_no"
    CHOICE = "choice"


class QuestionComponentType(str, Enum):
    TEXT = "text"
    PARAGRAPH = "paragraph"


@dataclass(slots=True)
class QuestionField:
    key: str
    label: str
    component_type: QuestionComponentType

    placeholder: str = ""
    required: bool = True

    min_length: int | None = None
    max_length: int | None = None

    validator: QuestionValidatorType = QuestionValidatorType.NONE
    choices: set[str] | None = None


@dataclass(slots=True)
class QuestionStep:
    fields: list[QuestionField] = field(default_factory=list)


@dataclass(slots=True)
class Questionnaire:
    title: str
    fields: list[QuestionField]
    steps: list[QuestionStep] = field(default_factory=list)
    description: str = ""

    delivery: Delivery = field(
        default_factory=lambda: Delivery(
            destination=MessageDestination.DIRECT_MESSAGE,
            visibility=MessageVisibility.PRIVATE,
        )
    )


@dataclass(slots=True)
class QuestionnaireResult:
    answers: dict[str, Any]
    completed: bool
