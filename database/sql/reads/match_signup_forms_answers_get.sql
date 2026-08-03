-- 讀取單一 match_signup_forms_player_answers（不輸出輸入用的 guild_id, thread_id, discord_id, field_key）
-- params: guild_id, thread_id, discord_id, field_key
-- returns: answer, submitted_at, updated_at
SELECT answer, submitted_at, updated_at
FROM match_signup_forms_player_answers
WHERE guild_id = :guild_id AND thread_id = :thread_id AND discord_id = :discord_id AND field_key = :field_key;
