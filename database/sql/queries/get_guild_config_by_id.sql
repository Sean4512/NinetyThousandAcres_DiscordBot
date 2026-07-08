SELECT
    field_key,
    config_value
FROM guild_configs
WHERE
    guild_id = ?
ORDER BY id ASC;