-- 刪除一筆 player_profiles_answers
-- params: guild_id, discord_id, field_key
DELETE FROM player_profiles_answers
WHERE guild_id = :guild_id AND discord_id = :discord_id AND field_key = :field_key;
