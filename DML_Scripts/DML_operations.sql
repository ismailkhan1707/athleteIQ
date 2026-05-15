SET SQL_SAFE_UPDATES = 0;
USE athleteiq;

UPDATE athletes
SET    status = 'inactive'
WHERE  athlete_id = 5;

UPDATE injury_records
SET    recovery_status = 'recovered'
WHERE  recovery_status = 'ongoing'
AND    date_occurred < '2023-01-01';


DELETE FROM injury_records
WHERE  injury_id = 10;

DELETE FROM performance_stats
WHERE  recorded_on < '2022-06-01';

SELECT 'DML operations complete.' AS status;
SET SQL_SAFE_UPDATES = 1;
