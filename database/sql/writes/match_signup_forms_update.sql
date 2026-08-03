-- 更新一筆 match_signup_forms 的可變欄位
-- params: guild_id, thread_id, message_id, status, title, content, log, updated_at
UPDATE match_signup_forms SET
    message_id = :message_id,
    status     = :status,
    title      = :title,
    content    = :content,
    log        = :log,
    updated_at = :updated_at
WHERE guild_id = :guild_id AND thread_id = :thread_id;
