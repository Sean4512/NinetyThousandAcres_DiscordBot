SELECT
    discord_id
FROM match_signup_forms_participants
WHERE guild_id = ?
  AND thread_id = ?
ORDER BY created_at ASC;