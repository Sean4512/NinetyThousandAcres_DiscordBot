SELECT
    field_key,
    answer
FROM player_profile_answers
WHERE
    discord_id = ?
    AND guild_id = ?
ORDER BY id ASC;