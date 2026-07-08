SELECT
    field_key,
    answer
FROM match_signup_forms_player_answers
WHERE
    guild_id = ?
    AND thread_id = ?
    AND discord_id = ?
ORDER BY id ASC;