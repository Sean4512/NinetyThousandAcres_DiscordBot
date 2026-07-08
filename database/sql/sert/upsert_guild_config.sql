INSERT INTO guild_configs (
    guild_id,
    field_key,
    config_value,
    created_at,
    updated_at
) VALUES (?, ?, ?, ?, ?)
ON CONFLICT(guild_id, field_key)
DO UPDATE SET
    config_value = excluded.config_value,
    updated_at = excluded.updated_at;

