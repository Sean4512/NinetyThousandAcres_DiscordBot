CREATE TABLE IF NOT EXISTS player_profile_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    discord_id TEXT NOT NULL,
    guild_id TEXT NOT NULL,

    field_key TEXT NOT NULL,
    field_label TEXT NOT NULL,
    answer TEXT,

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    UNIQUE(discord_id, guild_id, field_key),

    FOREIGN KEY (discord_id, guild_id)
        REFERENCES player_profiles(discord_id, guild_id)
        ON DELETE CASCADE
);