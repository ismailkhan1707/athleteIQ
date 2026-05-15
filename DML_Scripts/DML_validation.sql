USE athleteiq;


SELECT 'sports'              AS table_name, COUNT(*) AS row_count FROM sports
UNION ALL
SELECT 'athletes',                          COUNT(*)              FROM athletes
UNION ALL
SELECT 'athlete_enrollments',               COUNT(*)              FROM athlete_enrollments
UNION ALL
SELECT 'injury_records',                    COUNT(*)              FROM injury_records
UNION ALL
SELECT 'performance_stats',                 COUNT(*)              FROM performance_stats;



SELECT 'athletes - full_name NULL'    AS check_name, COUNT(*) AS null_count
FROM athletes WHERE full_name IS NULL
UNION ALL
SELECT 'athletes - date_of_birth NULL', COUNT(*)
FROM athletes WHERE date_of_birth IS NULL
UNION ALL
SELECT 'athletes - status NULL',        COUNT(*)
FROM athletes WHERE status IS NULL
UNION ALL
SELECT 'injury_records - injury_type NULL', COUNT(*)
FROM injury_records WHERE injury_type IS NULL
UNION ALL
SELECT 'injury_records - date_occurred NULL', COUNT(*)
FROM injury_records WHERE date_occurred IS NULL
UNION ALL
SELECT 'performance_stats - metric_name NULL', COUNT(*)
FROM performance_stats WHERE metric_name IS NULL
UNION ALL
SELECT 'performance_stats - value NULL', COUNT(*)
FROM performance_stats WHERE value IS NULL;


SELECT 'athlete_enrollments → athletes FK' AS check_name,
       COUNT(*) AS orphaned_rows
FROM   athlete_enrollments ae
LEFT JOIN athletes a ON ae.athlete_id = a.athlete_id
WHERE  a.athlete_id IS NULL;


SELECT 'athlete_enrollments → sports FK' AS check_name,
       COUNT(*) AS orphaned_rows
FROM   athlete_enrollments ae
LEFT JOIN sports s ON ae.sport_id = s.sport_id
WHERE  s.sport_id IS NULL;


SELECT 'injury_records → athletes FK' AS check_name,
       COUNT(*) AS orphaned_rows
FROM   injury_records ir
LEFT JOIN athletes a ON ir.athlete_id = a.athlete_id
WHERE  a.athlete_id IS NULL;


SELECT 'performance_stats → athletes FK' AS check_name,
       COUNT(*) AS orphaned_rows
FROM   performance_stats ps
LEFT JOIN athletes a ON ps.athlete_id = a.athlete_id
WHERE  a.athlete_id IS NULL;



SELECT 'performance_stats → sports FK' AS check_name,
       COUNT(*) AS orphaned_rows
FROM   performance_stats ps
LEFT JOIN sports s ON ps.sport_id = s.sport_id
WHERE  s.sport_id IS NULL;



SELECT 'Validation complete. All orphaned_rows values should be 0.' AS note;
