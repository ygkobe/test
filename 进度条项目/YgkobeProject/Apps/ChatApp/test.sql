-- 根据日期进行分组
SELECT DATE(create_time) AS day, COUNT(*) AS count
FROM history
GROUP BY DATE(create_time) ORDER by DATE(create_time) DESC;



-- 更新数据
update history set ip='127.0.0.2', create_time='2024-07-27 00:00:00' where id=8;




SELECT
    hours.hour_created,
    COALESCE(hist.count_per_hour, 0) AS count_per_hour
FROM
    (
        SELECT 0 AS hour_created
        UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL
        SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
        SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL
        SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL
        SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL
        SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL
        SELECT 19 UNION ALL SELECT 20 UNION ALL SELECT 21 UNION ALL
        SELECT 22 UNION ALL SELECT 23
    ) AS hours
LEFT JOIN (
    SELECT
        DATE_FORMAT(create_time, '%H') AS hour_created,
        COUNT(*) AS count_per_hour
    FROM
        history
    GROUP BY
        hour_created
) AS hist ON hours.hour_created = hist.hour_created
ORDER BY
    hours.hour_created;


select ip from history group by DATE(create_time)


SELECT
            ip,

            COUNT(*) AS count
        FROM
            history
        WHERE
            DATE(create_time) IN ('2024-07-27', '2024-07-26', '2024-07-25', '2024-07-24', '2024-07-23', '2024-07-22', '2024-07-21')
        GROUP BY
            ip
        ORDER BY
            count DESC limit 5;



select question from history order by create_time DESC limit 100;