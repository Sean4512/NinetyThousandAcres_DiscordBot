--CREATE TABLE IF NOT EXISTS guild_configs (
--    guild_id TEXT PRIMARY KEY, -- 群組ID
--    guild_name TEXT NOT NULL, -- -- 群組名稱
--    is_initialized INTEGER NOT NULL DEFAULT 0,
--    admin_role_id TEXT, -- 身分組ID
--    category_id TEXT,
--    created_at TEXT NOT NULL,
--    updated_at TEXT NOT NULL
--);


CREATE TABLE IF NOT EXISTS guild_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    guild_id TEXT NOT NULL,

    field_key TEXT NOT NULL,      -- 設定名稱，例如 admin_role_id, category_id
    config_value TEXT,            -- 設定值，例如 role id, category id, true/false

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    UNIQUE(guild_id, field_key),

    FOREIGN KEY (guild_id)
        REFERENCES guild_profile(guild_id)
        ON DELETE CASCADE
);