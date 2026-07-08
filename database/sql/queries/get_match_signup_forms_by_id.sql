SELECT

    forum_id,
    message_id,
    status,
    title,
    content,
    log,
    created_at,
    updated_at

FROM match_signup_forms

WHERE guild_id = ? AND  thread_id = ?;