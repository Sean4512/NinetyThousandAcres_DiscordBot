INSERT INTO match_signup_forms_participants (

    guild_id,
    thread_id,
    discord_id,
    created_at

) VALUES (?, ?, ?, ?)
ON CONFLICT(guild_id, thread_id, discord_id)
DO NOTHING;
