CREATE TABLE IF NOT EXISTS match_signup_forms (

    guild_id TEXT NOT NULL,
    forum_id TEXT NOT NULL,
    thread_id TEXT NOT NULL,
    message_id TEXT NOT NULL,
    status TEXT NOT NULL,

    title TEXT NOT NULL,
    content TEXT,
    log TEXT,

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    PRIMARY KEY (guild_id, thread_id),

    FOREIGN KEY (guild_id) REFERENCES guild_profile(guild_id) ON DELETE CASCADE
);