-- 刪除一筆 player_profiles（會透過 FK CASCADE 連帶刪除其 answers）
-- params: guild_id, discord_id
DELETE FROM player_profiles
WHERE guild_id = :guild_id AND discord_id = :discord_id;
