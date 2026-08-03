CREATE TABLE IF NOT EXISTS match_signup_forms_player_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    guild_id TEXT NOT NULL,
    thread_id TEXT NOT NULL,
    discord_id TEXT NOT NULL,

    field_key TEXT NOT NULL,
    answer TEXT,

    submitted_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    UNIQUE(guild_id, thread_id, discord_id, field_key),

    FOREIGN KEY (guild_id, thread_id, discord_id)
        REFERENCES match_signup_forms_participants(guild_id, thread_id, discord_id)
        ON DELETE CASCADE

);

