-- 讀取單一 player_profiles_answers（不輸出輸入用的 guild_id, discord_id, field_key）
-- params: guild_id, discord_id, field_key
-- returns: field_label, answer, submitted_at, updated_at
SELECT field_label, answer, submitted_at, updated_at
FROM player_profiles_answers
WHERE guild_id = :guild_id AND discord_id = :discord_id AND field_key = :field_key;
