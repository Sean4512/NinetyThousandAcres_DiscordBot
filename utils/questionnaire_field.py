# -*- coding: utf-8 -*-
"""
@File    : questionnaire_field.py
@Time    : 2026/7/1 上午 01:38
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""


from pathlib import Path
from typing import Any

import yaml

from utils.models.questionnaire import *
from utils.models.discord_delivery import Delivery, MessageDestination, MessageVisibility

def load_questionnaire_fields_from_yaml(file_path: str | Path) -> Questionnaire:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"找不到註冊欄位設定檔: {path}")

    with path.open("r", encoding="utf-8") as file:
        data: dict[str, Any] = yaml.safe_load(file) or {}

    field_name: str = data.get("field_name", "表單")

    destination = data.get("destination", "direct_message")
    visibility = data.get("visibility", "private")

    raw_fields = data.get("field_list")

    if not isinstance(raw_fields, list):
        raise ValueError(f"FIELDS_YAML({path}) 必須包含 field_list 陣列。")

    fields: list[QuestionField] = []

    seen_keys: set[str] = set()

    for index, item in enumerate(raw_fields, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"第 {index} 個欄位設定必須是 object。")

        key = item.get("key")
        label = item.get("label")
        component_type = item.get("component_type")

        if not key or not isinstance(key, str):
            raise ValueError(f"第 {index} 個欄位缺少 key。")

        if key in seen_keys:
            raise ValueError(f"欄位 key 重複: {key}")

        if not label or not isinstance(label, str):
            raise ValueError(f"欄位 {key} 缺少 label。")

        if not component_type or not isinstance(component_type, str):
            raise ValueError(f"欄位 {key} 缺少 component_type。")

        seen_keys.add(key)

        choices = item.get("choices", set())

        fields.append(
            QuestionField(
                key=key,
                label=label,
                component_type=QuestionComponentType(component_type),
                placeholder=item.get("placeholder", ""),
                required=item.get("required", True),
                min_length=item.get("min_length"),
                max_length=item.get("max_length"),
                validator=QuestionValidatorType(
                    item.get("validator", QuestionValidatorType.NONE.value)
                ),
                choices=set(choices),
            )
        )

    if not fields:
        raise ValueError(f"FIELDS_YAML({path}) 不可沒有任何欄位。")

    questionnaire = Questionnaire(
        title=field_name,
        fields=fields,
        delivery=Delivery(
            destination=MessageDestination(destination),
            visibility=MessageVisibility(visibility),
        ),
    )

    return questionnaire

def build_questionnaire_steps(fields: list[QuestionField]) -> list[QuestionStep]:

    steps: list[QuestionStep] = []
    buffer: list[QuestionField] = []

    def flush_buffer() -> None:
        nonlocal buffer

        while buffer:
            chunk = buffer[:5]
            steps.append(QuestionStep(fields=chunk))
            buffer = buffer[5:]

    for field in fields:
        if field.component_type == QuestionComponentType.TEXT:
            buffer.append(field)

            if len(buffer) >= 5:
                flush_buffer()

        elif field.component_type == QuestionComponentType.PARAGRAPH:
            flush_buffer()
            steps.append(QuestionStep(fields=[field]))

        else:
            raise ValueError(f"Modal 不支援此欄位類型: {field.component_type}")

    flush_buffer()

    if not steps:
        raise ValueError("FIELDS 不可為空。")

    return steps

def validate_questionnaire_field(
    field: QuestionField,
    raw_value: str,
) -> tuple[bool, Any, str | None]:
    """
    驗證單一欄位，並回傳正規化後的值。

    回傳：
        success: 是否驗證成功
        value: 正規化後的值
        error_message: 錯誤訊息
    """
    value = raw_value.strip()

    if not value:
        if field.required:
            return False, None, f"「{field.label}」為必填欄位。"

        return True, None, None

    if field.validator == QuestionValidatorType.NONE:
        return True, value, None

    if field.validator == QuestionValidatorType.INT:
        if not value.isdigit():
            return False, None, f"「{field.label}」只能輸入整數。"

        return True, int(value), None

    if field.validator == QuestionValidatorType.YES_NO:
        normalized = value.upper()

        yes_values = {"Y", "YES", "是", "對", "有", "1"}
        no_values = {"N", "NO", "否", "不", "沒有", "0"}

        if normalized in yes_values or value in yes_values:
            return True, 1, None

        if normalized in no_values or value in no_values:
            return True, 0, None

        return False, None, f"「{field.label}」只能輸入 Y、N、是、否。"

    if field.validator == QuestionValidatorType.CHOICE:
        if field.choices is None:
            return False, None, f"「{field.label}」尚未設定可用選項。"

        normalized_choices = {choice.lower() for choice in field.choices}

        if value.lower() not in normalized_choices:
            allowed = "、".join(sorted(field.choices))
            return False, None, f"「{field.label}」只能輸入：{allowed}。"

        return True, value.lower(), None

    return False, None, f"「{field.label}」使用了未知的驗證規則。"

