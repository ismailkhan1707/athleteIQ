USE athleteiq;

CREATE TABLE performance_stats (
  stat_id     SERIAL      PRIMARY KEY,
  athlete_id  INT         NOT NULL REFERENCES athletes(athlete_id) ON DELETE CASCADE,
  sport_id    INT         NOT NULL REFERENCES sports(sport_id)   ON DELETE CASCADE,
  metric_name VARCHAR(80) NOT NULL,
  value       NUMERIC(10,3) NOT NULL,
  recorded_on DATE        NOT NULL DEFAULT (CURRENT_DATE)
);