-- 讀取某 guild 的所有 player_profiles（不輸出輸入用的 guild_id）
-- params: guild_id
-- returns: discord_id, submitted_at（多列）
SELECT discord_id, submitted_at
FROM player_profiles
WHERE guild_id = :guild_id
ORDER BY submitted_at;
