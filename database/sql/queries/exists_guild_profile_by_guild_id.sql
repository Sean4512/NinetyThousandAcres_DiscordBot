SELECT EXISTS (
    SELECT 1
    FROM guild_profile
    WHERE guild_id = ?
);