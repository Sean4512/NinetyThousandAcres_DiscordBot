-- 檢查 guild_profiles 是否存在
-- params: guild_id
-- returns: is_exists（1 存在 / 0 不存在）
SELECT EXISTS(
    SELECT 1
    FROM guild_profiles
    WHERE guild_id = :guild_id
) AS is_exists;
