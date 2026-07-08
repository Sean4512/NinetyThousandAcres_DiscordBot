--CREATE TABLE IF NOT EXISTS player_profiles (
--    discord_id TEXT NOT NULL,
--    guild_id TEXT NOT NULL,
--    occupation TEXT,
--    country TEXT,
--    age INTEGER,
--    gender TEXT,
--    is_single INTEGER, -- 使用 0 代表否，1 代表是
--    game_uid TEXT,
--    game_name TEXT,
--    online_time TEXT,
--    notes TEXT,       -- 玩家自己填寫的備註
--    admin_notes TEXT, -- 管理員給予的備註
--    created_at TEXT NOT NULL,
--    updated_at TEXT NOT NULL,
--    PRIMARY KEY (discord_id, guild_id),
--    FOREIGN KEY (guild_id) REFERENCES guild_configs(guild_id) ON DELETE CASCADE
--);


CREATE TABLE IF NOT EXISTS player_profiles (
    discord_id TEXT NOT NULL,
    guild_id TEXT NOT NULL,
    admin_notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    PRIMARY KEY (discord_id, guild_id),
    FOREIGN KEY (guild_id) REFERENCES guild_profile(guild_id) ON DELETE CASCADE
);