--CREATE TABLE IF NOT EXISTS guild_configs (
--    guild_id TEXT PRIMARY KEY, -- 群組ID
--    guild_name TEXT NOT NULL, -- -- 群組名稱
--    is_initialized INTEGER NOT NULL DEFAULT 0,
--    admin_role_id TEXT, -- 身分組ID
--    category_id TEXT,
--    created_at TEXT NOT NULL,
--    updated_at TEXT NOT NULL
--);


CREATE TABLE IF NOT EXISTS guild_profile (
    guild_id TEXT PRIMARY KEY, -- Discord 群組 ID

    created_at TEXT NOT NULL
);