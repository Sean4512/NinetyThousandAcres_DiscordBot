INSERT INTO match_signup_forms (

    guild_id,
    forum_id,
    thread_id,
    message_id,
    status,
    title,
    content,
    log,
    created_at,
    updated_at

) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(guild_id, thread_id)
DO UPDATE SET
    status = excluded.status,
    title = excluded.title,
    content = excluded.content,
    log = excluded.log,
    updated_at = excluded.updated_at;