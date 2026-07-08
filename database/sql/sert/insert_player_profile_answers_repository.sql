INSERT INTO player_profile_answers (
    guild_id,
    discord_id,
    field_key,
    field_label,
    answer,
    created_at,
    updated_at
) VALUES (?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(discord_id, guild_id, field_key)
DO UPDATE SET
    field_label = excluded.field_label,
    answer = excluded.answer,
    updated_at = excluded.updated_at;