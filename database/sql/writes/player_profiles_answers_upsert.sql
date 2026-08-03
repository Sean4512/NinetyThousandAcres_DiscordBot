-- 新增或更新一筆 player_profiles_answers（依 UNIQUE(guild_id, discord_id, field_key)）
-- params: guild_id, discord_id, field_key, field_label, answer, submitted_at, updated_at
INSERT INTO player_profiles_answers (guild_id, discord_id, field_key, field_label, answer, submitted_at, updated_at)
VALUES (:guild_id, :discord_id, :field_key, :field_label, :answer, :submitted_at, :updated_at)
ON CONFLICT(guild_id, discord_id, field_key) DO UPDATE SET
    field_label = excluded.field_label,
    answer      = excluded.answer,
    updated_at  = excluded.updated_at;
