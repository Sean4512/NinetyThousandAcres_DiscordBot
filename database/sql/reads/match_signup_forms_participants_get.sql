-- 讀取單一 match_signup_forms_participants（不輸出輸入用的 guild_id, thread_id, discord_id）
-- params: guild_id, thread_id, discord_id
-- returns: submitted_at
SELECT submitted_at
FROM match_signup_forms_participants
WHERE guild_id = :guild_id AND thread_id = :thread_id AND discord_id = :discord_id;
