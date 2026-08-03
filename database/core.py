# -*- coding: utf-8 -*-
"""
@File    : core.py
@Time    : 2026/6/30 下午 05:52
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

import sqlite3
from collections.abc import Mapping, Sequence
from database.connection import get_discord_database_connection

Params = Mapping | Sequence


class BaseRepository:

    @staticmethod
    def run_sql_execute(sql_content: str, parameters: Params = ()) -> int:
        """
        寫入類（create / insert / update / delete）
        :param sql_content:
        :param parameters:
        :return: 受影響的列數（rowcount）；ON CONFLICT DO NOTHING 衝突時為 0；CREATE 等 DDL 為 -1
        """
        conn = get_discord_database_connection()
        try:
            cursor = conn.execute(sql_content, parameters)
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()  # 無論成功失敗都要關

    @staticmethod
    def run_sql_fetchall(sql_content: str, parameters: Params = ()) -> list[sqlite3.Row]:
        """
        讀取多列
        :param sql_content:
        :param parameters:
        :return:
        """
        conn = get_discord_database_connection()
        try:
            cursor = conn.execute(sql_content, parameters)
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def run_sql_fetchone(sql_content: str, parameters: Params = ()) -> sqlite3.Row | None:
        """
        讀取單列（單一 profile、exists 檢查、單一設定值）
        :param sql_content:
        :param parameters:
        :return:
        """
        conn = get_discord_database_connection()
        try:
            cursor = conn.execute(sql_content, parameters)
            return cursor.fetchone()
        finally:
            conn.close()


