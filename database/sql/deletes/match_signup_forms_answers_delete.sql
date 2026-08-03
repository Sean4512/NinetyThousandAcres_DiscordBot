-- 刪除一筆 match_signup_forms_player_answers
-- params: guild_id, thread_id, discord_id, field_key
DELETE FROM match_signup_forms_player_answers
WHERE guild_id = :guild_id AND thread_id = :thread_id AND discord_id = :discord_id AND field_key = :field_key;
