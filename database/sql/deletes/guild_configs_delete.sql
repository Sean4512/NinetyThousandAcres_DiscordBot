-- 刪除一筆 guild_configs
-- params: guild_id, field_key
DELETE FROM guild_configs
WHERE guild_id = :guild_id AND field_key = :field_key;
