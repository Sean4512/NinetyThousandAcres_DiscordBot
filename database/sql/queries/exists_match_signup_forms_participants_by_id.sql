
SELECT EXISTS (
    SELECT 1
    FROM match_signup_forms_participants
    WHERE guild_id = ? AND  thread_id = ? AND  discord_id = ?
);

