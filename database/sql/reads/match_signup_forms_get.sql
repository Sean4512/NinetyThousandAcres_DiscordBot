-- 讀取單一 match_signup_forms（不輸出輸入用的 guild_id, thread_id）
-- params: guild_id, thread_id
-- returns: forum_id, message_id, status, title, content, log, submitted_at, updated_at
SELECT forum_id, message_id, status, title, content, log, submitted_at, updated_at
FROM match_signup_forms
WHERE guild_id = :guild_id AND thread_id = :thread_id;
