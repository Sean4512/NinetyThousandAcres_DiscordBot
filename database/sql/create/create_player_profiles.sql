
CREATE TABLE IF NOT EXISTS player_profiles (
    guild_id TEXT NOT NULL,
    discord_id TEXT NOT NULL,

    submitted_at TEXT NOT NULL,

    PRIMARY KEY (guild_id, discord_id),
    FOREIGN KEY (guild_id) REFERENCES guild_profiles(guild_id) ON DELETE CASCADE
);
