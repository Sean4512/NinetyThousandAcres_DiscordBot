-- 讀取某玩家的所有 player_profiles_answers（不輸出輸入用的 guild_id, discord_id）
-- params: guild_id, discord_id
-- returns: field_key, field_label, answer, submitted_at, updated_at（多列）
SELECT field_key, field_label, answer, submitted_at, updated_at
FROM player_profiles_answers
WHERE guild_id = :guild_id AND discord_id = :discord_id
ORDER BY field_key;
