CREATE VIEW `ros_user_tags_count` AS
SELECT tags_cnt.user_id, tags_count, tags_extended_count - tags_count as extended_tags_count
FROM 
(
	SELECT user_id, count(*) as tags_count
	FROM ra_user_tag
	GROUP BY user_id
) as tags_cnt 
JOIN (
	SELECT user_id, count(*) as tags_extended_count 
	FROM ra_user_tag_extended
	GROUP BY user_id
) as tags_ext_cnt
ON tags_cnt.user_id = tags_ext_cnt.user_id
