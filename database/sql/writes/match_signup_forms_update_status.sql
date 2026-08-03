-- 只更新一筆 match_signup_forms 的 status
-- params: guild_id, thread_id, status, updated_at
UPDATE match_signup_forms SET
    status     = :status,
    updated_at = :updated_at
WHERE guild_id = :guild_id AND thread_id = :thread_id;
