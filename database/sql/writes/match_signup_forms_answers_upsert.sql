-- 新增或更新一筆 match_signup_forms_player_answers（依 UNIQUE(guild_id, thread_id, discord_id, field_key)）
-- params: guild_id, thread_id, discord_id, field_key, answer, submitted_at, updated_at
INSERT INTO match_signup_forms_player_answers (guild_id, thread_id, discord_id, field_key, answer, submitted_at, updated_at)
VALUES (:guild_id, :thread_id, :discord_id, :field_key, :answer, :submitted_at, :updated_at)
ON CONFLICT(guild_id, thread_id, discord_id, field_key) DO UPDATE SET
    answer     = excluded.answer,
    updated_at = excluded.updated_at;
