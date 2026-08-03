-- 新增或更新一筆 guild_configs（依 UNIQUE(guild_id, field_key)）
-- params: guild_id, field_key, config_value, submitted_at, updated_at
INSERT INTO guild_configs (guild_id, field_key, config_value, submitted_at, updated_at)
VALUES (:guild_id, :field_key, :config_value, :submitted_at, :updated_at)
ON CONFLICT(guild_id, field_key) DO UPDATE SET
    config_value = excluded.config_value,
    updated_at   = excluded.updated_at;
