
CREATE TABLE IF NOT EXISTS guild_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    guild_id TEXT NOT NULL,

    field_key TEXT NOT NULL,      -- 設定名稱，例如 admin_role_id, category_id
    config_value TEXT,            -- 設定值，例如 role id, category id, true/false

    submitted_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    UNIQUE(guild_id, field_key),

    FOREIGN KEY (guild_id)
        REFERENCES guild_profiles(guild_id)
        ON DELETE CASCADE
);
