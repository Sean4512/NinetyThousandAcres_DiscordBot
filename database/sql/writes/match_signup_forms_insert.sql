-- 新增一筆 match_signup_forms
-- params: guild_id, forum_id, thread_id, message_id, status, title, content, log, submitted_at, updated_at
INSERT INTO match_signup_forms (guild_id, forum_id, thread_id, message_id, status, title, content, log, submitted_at, updated_at)
VALUES (:guild_id, :forum_id, :thread_id, :message_id, :status, :title, :content, :log, :submitted_at, :updated_at);
