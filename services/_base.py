# -*- coding: utf-8 -*-
"""
@File    : _base.py
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : Service 共用工具：時間戳產生、sqlite3.Row -> dict 轉換
"""

import sqlite3
from datetime import datetime, timezone
from typing import Any


class BaseService:
    """
    所有 service 的共用基底。

    Service 是 bot/commands（cog）與 database/repositories 之間的中間層，負責：
      - 產生 submitted_at / updated_at 時間戳（repository 不再由 cog 傳入時間）
      - 跨 repository 的商業邏輯編排
      - 把 sqlite3.Row 轉成純 dict，讓 cog 不必碰 sqlite 型別
      - 把 DB 例外（如 IntegrityError）翻譯成 domain 例外
    """

    @staticmethod
    def _now() -> str:
        """回傳目前 UTC 時間的 ISO 8601 字串（秒精度），寫入 TEXT 欄位用。"""
        return datetime.now(timezone.utc).isoformat(timespec="seconds")

    @staticmethod
    def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
        """把單一 sqlite3.Row 轉成 dict；None 原樣回傳。"""
        return dict(row) if row is not None else None

    @staticmethod
    def _rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
        """把多列 sqlite3.Row 轉成 list[dict]。"""
        return [dict(row) for row in rows]
