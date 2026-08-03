-- 新增一筆 match_signup_forms_participants
-- params: guild_id, thread_id, discord_id, submitted_at
INSERT INTO match_signup_forms_participants (guild_id, thread_id, discord_id, submitted_at)
VALUES (:guild_id, :thread_id, :discord_id, :submitted_at);
