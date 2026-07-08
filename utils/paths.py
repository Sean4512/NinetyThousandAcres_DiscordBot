# -*- coding: utf-8 -*-
"""
@File    : paths.py
@Time    : 2026/4/14 下午 09:33
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from pathlib import Path


g_project_root = Path(__file__).resolve().parent.parent
g_sql_dir = g_project_root / "database" / "sql"