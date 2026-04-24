USE athleteiq;

CREATE INDEX idx_injuries_athlete   ON injury_records(athlete_id);
CREATE INDEX idx_perf_athlete_sport  ON performance_stats(athlete_id, sport_id);
CREATE INDEX idx_athletes_status     ON athletes(status);