-- 讀取某 guild 的所有 match_signup_forms（不輸出輸入用的 guild_id）
-- params: guild_id
-- returns: thread_id, forum_id, message_id, status, title, content, log, submitted_at, updated_at（多列）
SELECT thread_id, forum_id, message_id, status, title, content, log, submitted_at, updated_at
FROM match_signup_forms
WHERE guild_id = :guild_id
ORDER BY submitted_at;
