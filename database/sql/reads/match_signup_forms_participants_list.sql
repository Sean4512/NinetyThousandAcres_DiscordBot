-- 讀取某報名表的所有參與者（不輸出輸入用的 guild_id, thread_id）
-- params: guild_id, thread_id
-- returns: discord_id, submitted_at（多列）
SELECT discord_id, submitted_at
FROM match_signup_forms_participants
WHERE guild_id = :guild_id AND thread_id = :thread_id
ORDER BY submitted_at;
