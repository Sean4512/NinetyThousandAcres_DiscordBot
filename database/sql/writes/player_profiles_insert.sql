-- 新增一筆 player_profiles
-- params: guild_id, discord_id, submitted_at
INSERT INTO player_profiles (guild_id, discord_id, submitted_at)
VALUES (:guild_id, :discord_id, :submitted_at);
