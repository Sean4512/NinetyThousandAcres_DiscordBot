# Ninety Thousand Acres — Discord Bot

一個以 [discord.py](https://github.com/Rapptz/discord.py) 打造的 Discord 機器人，提供玩家註冊、賽事報名與問卷等功能，採用 YAML 設定驅動欄位、SQLite 儲存資料。

> ⚠️ 本專案目前位於 `sketch` 分支（草稿階段）。

## 功能特色

- **玩家註冊（Player Register）**：透過互動式表單收集並儲存玩家資料。
- **賽事報名（Match Signup）**：建立報名表單、管理參加者與其填答內容。
- **問卷系統（Questionnaire）**：以 Modal / View 元件組成的可重用問卷流程。
- **伺服器設定（Guild Setup）**：針對各 Discord 伺服器儲存專屬設定。
- **YAML 欄位設定**：報名/註冊欄位皆由 `cfg/` 下的 YAML 檔定義，免改程式即可調整。
- **SQLite 資料庫**：內建建表、查詢、寫入用的 SQL 腳本。

## 技術棧

- Python 3
- discord.py
- python-dotenv
- PyYAML
- SQLite

## 專案結構

```
.
├── main.py                 # 進入點：載入設定、初始化資料庫、啟動 Bot
├── bot/                    # Discord Bot 主體
│   ├── client.py           # 建立 Bot 實例
│   ├── commands/           # 各項指令（玩家註冊、賽事報名、問卷等）
│   ├── core/               # Cog / Modal / View 基底類別
│   └── test_commands/      # 測試用指令
├── config/                 # 設定載入與檢查
├── cfg/                    # YAML 欄位與擴充設定
├── database/               # 資料庫連線、初始化與 SQL 腳本
│   ├── repositories/       # 資料存取層
│   └── sql/                # create / queries / insert / delete SQL
├── services/               # 商業邏輯層
├── utils/                  # 共用工具（logger、例外、型別等）
├── tests/                  # 測試
└── requirements.txt        # 相依套件
```

## 安裝與執行

### 1. 建立虛擬環境並安裝相依套件

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. 設定環境變數

在專案根目錄建立 `.env` 檔（此檔已被 `.gitignore` 排除，切勿上傳）：

```dotenv
# NINETY_THOUSAND_ACRES
NINETY_THOUSAND_ACRES_PLAYER_REGISTER_FIELDS_YAML_PATH="./cfg/player_register_fields.yaml"
NINETY_THOUSAND_ACRES_MATCH_SIGNUP_FIELDS_YAML_PATH="./cfg/match_signup_fields.yaml"

# Discord Bot
NINETY_THOUSAND_ACRES_DISCORD_BOT_TOKEN=你的_DISCORD_BOT_TOKEN
NINETY_THOUSAND_ACRES_DISCORD_BOT_SYNCED_COMMAND=0
NINETY_THOUSAND_ACRES_DISCORD_BOT_SYNCED_COMMAND_FOR_DEBUG=0
NINETY_THOUSAND_ACRES_DISCORD_GUILD_ID_FOR_DEBUG=你的_測試伺服器_ID
NINETY_THOUSAND_ACRES_DISCORD_BOT_EXTENSIONS_YAML_PATH="cfg/bot_extensions.yaml"
NINETY_THOUSAND_ACRES_DISCORD_BOT_COMMAND_PREFIX="!"
NINETY_THOUSAND_ACRES_DISCORD_BOT_PLAYER_REGISTER_TIMEOUT=300

# App log
NINETY_THOUSAND_ACRES_LOG_DIRECTORY="./logs"
NINETY_THOUSAND_ACRES_BOT_LOG_LEVEL=DEBUG
NINETY_THOUSAND_ACRES_GOOGLE_LOG_LEVEL=DEBUG

# Database
NINETY_THOUSAND_ACRES_DATABASE_DIRECTORY="./data/db"
NINETY_THOUSAND_ACRES_DATABASE_DISCORD_FILE="NinetyThousandAcres_discord.db"
NINETY_THOUSAND_ACRES_DATABASE_URL=sqlite:///data/db/app.db
```

> Token 請至 [Discord Developer Portal](https://discord.com/developers/applications) 取得，並妥善保管、切勿外流。

### 3. 啟動 Bot

```bash
python main.py
```

啟動時會依序載入設定、檢查 logger、初始化資料庫，最後啟動 Discord Bot。

## 授權

本專案尚未指定授權條款（All rights reserved）。
