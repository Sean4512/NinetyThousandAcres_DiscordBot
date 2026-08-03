-- 讀取單一 player_profiles（不輸出輸入用的 guild_id, discord_id）
-- params: guild_id, discord_id
-- returns: submitted_at
SELECT submitted_at
FROM player_profiles
WHERE guild_id = :guild_id AND discord_id = :discord_id;
