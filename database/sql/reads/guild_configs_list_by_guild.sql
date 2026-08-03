-- 讀取某 guild 的所有 guild_configs（不輸出輸入用的 guild_id）
-- params: guild_id
-- returns: field_key, config_value, submitted_at, updated_at（多列）
SELECT field_key, config_value, submitted_at, updated_at
FROM guild_configs
WHERE guild_id = :guild_id
ORDER BY field_key;
