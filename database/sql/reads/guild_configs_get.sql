-- 讀取單一 guild_configs 設定值（不輸出輸入用的 guild_id, field_key）
-- params: guild_id, field_key
-- returns: config_value, submitted_at, updated_at
SELECT config_value, submitted_at, updated_at
FROM guild_configs
WHERE guild_id = :guild_id AND field_key = :field_key;
