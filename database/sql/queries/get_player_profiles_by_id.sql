SELECT
    discord_id,
    guild_id,
    admin_notes,
    created_at,
    updated_at
FROM player_profiles
WHERE guild_id = ? AND  discord_id = ?;