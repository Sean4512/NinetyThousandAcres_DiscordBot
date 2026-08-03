-- 刪除一筆 match_signup_forms_participants（會透過 FK CASCADE 連帶刪除該參與者的 answers）
-- params: guild_id, thread_id, discord_id
DELETE FROM match_signup_forms_participants
WHERE guild_id = :guild_id AND thread_id = :thread_id AND discord_id = :discord_id;
