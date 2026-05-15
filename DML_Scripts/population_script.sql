USE athleteiq;

SET GLOBAL local_infile = 1;

SET FOREIGN_KEY_CHECKS = 0;

-- 1. USERS (no FK dependencies)
LOAD DATA LOCAL INFILE 'D:/IMSciences/Database Systems Lab/Population_data/sports.csv'
INTO TABLE sports
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(sport_id, name, category);

-- 3. ATHLETES (no FK dependencies)
LOAD DATA LOCAL INFILE 'D:/IMSciences/Database Systems Lab/Population_data/athletes.csv'
INTO TABLE athletes
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(athlete_id, full_name, date_of_birth, gender, nationality, contact_info, status, created_at);

-- 4. ATHLETE_ENROLLMENTS (depends on athletes + sports)
LOAD DATA LOCAL INFILE 'D:/IMSciences/Database Systems Lab/Population_data/athlete_enrollments.csv'
INTO TABLE athlete_enrollments
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(athlete_id, sport_id, enrolled_on);

-- 5. INJURY_RECORDS (depends on athletes)
LOAD DATA LOCAL INFILE 'D:/IMSciences/Database Systems Lab/Population_data/injury_records.csv'
INTO TABLE injury_records
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(injury_id, athlete_id, injury_type, severity, date_occurred, recovery_status, notes);

-- 6. PERFORMANCE_STATS (depends on athletes + sports)
LOAD DATA LOCAL INFILE 'D:/IMSciences/Database Systems Lab/Population_data/performance_stats.csv'
INTO TABLE performance_stats
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(stat_id, athlete_id, sport_id, metric_name, value, recorded_on);

SET FOREIGN_KEY_CHECKS = 1;

SELECT 'Data load complete.' AS status;
