-- 檢查 match_signup_forms 是否存在
-- params: guild_id, thread_id
-- returns: is_exists（1 存在 / 0 不存在）
SELECT EXISTS(
    SELECT 1
    FROM match_signup_forms
    WHERE guild_id = :guild_id AND thread_id = :thread_id
) AS is_exists;
