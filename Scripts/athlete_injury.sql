USE athleteiq;

CREATE TABLE injury_records (
  injury_id       SERIAL      PRIMARY KEY,
  athlete_id      INT         NOT NULL REFERENCES athletes(athlete_id) ON DELETE CASCADE,
  injury_type     VARCHAR(100) NOT NULL,
  severity        VARCHAR(20) CHECK (severity IN ('mild', 'moderate', 'severe')),
  date_occurred   DATE        NOT NULL,
  recovery_status VARCHAR(30) NOT NULL DEFAULT 'ongoing'
                              CHECK (recovery_status IN ('ongoing', 'recovered', 'chronic')),
  notes           TEXT
);