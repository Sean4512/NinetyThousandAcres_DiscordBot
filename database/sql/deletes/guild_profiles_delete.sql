-- 刪除一筆 guild_profiles（會透過 FK CASCADE 連帶刪除其子資料）
-- params: guild_id
DELETE FROM guild_profiles
WHERE guild_id = :guild_id;
