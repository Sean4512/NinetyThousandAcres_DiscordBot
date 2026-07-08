# -*- coding: utf-8 -*-
"""
@File    : questionnaire.py
@Time    : 2026/6/12 下午 03:27
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class QuestionValidatorType(str, Enum):
    NONE = "none"
    INT = "int"
    YES_NO = "yes_no"
    CHOICE = "choice"


class QuestionComponentType(str, Enum):
    TEXT = "text"
    PARAGRAPH = "paragraph"


class QuestionnaireDestination(str, Enum):
    DIRECT_MESSAGE = "direct_message"
    CHANNEL = "channel"
    THREAD = "thread"

class QuestionnaireVisibility(str, Enum):
    PRIVATE = "private"
    EPHEMERAL = "ephemeral"
    PUBLIC = "public"

@dataclass(slots=True, frozen=True)
class QuestionnaireDelivery:
    destination: QuestionnaireDestination
    visibility: QuestionnaireVisibility

    def __post_init__(self) -> None:
        if (
                self.destination is QuestionnaireDestination.DIRECT_MESSAGE
                and self.visibility is not QuestionnaireVisibility.PRIVATE
        ):
            raise ValueError(
                "DIRECT_MESSAGE 只能搭配 PRIVATE visibility。"
            )

        if (
                self.destination in
                {
                    QuestionnaireDestination.CHANNEL,
                    QuestionnaireDestination.THREAD,
                }
                and self.visibility is QuestionnaireVisibility.PRIVATE
        ):
            raise ValueError(
                "CHANNEL 或 THREAD 不可搭配 PRIVATE visibility，"
                "請使用 EPHEMERAL 或 PUBLIC。"
            )

    @property
    def is_direct_message(self) -> bool:
        return self.destination is QuestionnaireDestination.DIRECT_MESSAGE

    @property
    def is_ephemeral(self) -> bool:
        return self.visibility is QuestionnaireVisibility.EPHEMERAL

    @property
    def is_public(self) -> bool:
        return self.visibility is QuestionnaireVisibility.PUBLIC

    @property
    def interaction_ephemeral(self) -> bool:
        return (
            not self.is_direct_message
            and self.is_ephemeral
        )


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

    delivery: QuestionnaireDelivery = field(
        default_factory=lambda: QuestionnaireDelivery(
            destination=QuestionnaireDestination.DIRECT_MESSAGE,
            visibility=QuestionnaireVisibility.PRIVATE,
        )
    )


@dataclass(slots=True)
class QuestionnaireResult:
    answers: dict[str, Any]
    completed: bool

