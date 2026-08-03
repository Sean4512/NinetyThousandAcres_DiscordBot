-- 讀取某參與者在某報名表的所有回答（不輸出輸入用的 guild_id, thread_id, discord_id）
-- params: guild_id, thread_id, discord_id
-- returns: field_key, answer, submitted_at, updated_at（多列）
SELECT field_key, answer, submitted_at, updated_at
FROM match_signup_forms_player_answers
WHERE guild_id = :guild_id AND thread_id = :thread_id AND discord_id = :discord_id
ORDER BY field_key;
