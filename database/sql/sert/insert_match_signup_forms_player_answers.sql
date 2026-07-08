INSERT INTO match_signup_forms_player_answers (

    guild_id,
    thread_id,
    discord_id,
    field_key,
    answer,
    created_at,
    updated_at

) VALUES (?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(guild_id, thread_id, discord_id, field_key)
DO UPDATE SET
    answer = excluded.answer,
    updated_at = excluded.updated_at;