-- 刪除一筆 match_signup_forms（會透過 FK CASCADE 連帶刪除 participants 與 answers）
-- params: guild_id, thread_id
DELETE FROM match_signup_forms
WHERE guild_id = :guild_id AND thread_id = :thread_id;
