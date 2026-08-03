-- 讀取單一 guild_profiles（不輸出輸入用的 guild_id）
-- params: guild_id
-- returns: submitted_at
SELECT submitted_at
FROM guild_profiles
WHERE guild_id = :guild_id;
