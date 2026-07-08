CREATE TABLE IF NOT EXISTS match_signup_forms_participants (

    guild_id TEXT NOT NULL,
    thread_id TEXT NOT NULL,
    discord_id TEXT NOT NULL,

    created_at TEXT NOT NULL,

    PRIMARY KEY (guild_id, thread_id, discord_id),

    FOREIGN KEY (guild_id, thread_id)
        REFERENCES match_signup_forms(guild_id, thread_id)
        ON DELETE CASCADE
);