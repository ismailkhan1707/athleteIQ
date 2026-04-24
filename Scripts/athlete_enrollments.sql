USE athleteiq;

CREATE TABLE athlete_enrollments (
  athlete_id  INT NOT NULL REFERENCES athletes(athlete_id) ON DELETE CASCADE,
  sport_id    INT NOT NULL REFERENCES sports(sport_id)   ON DELETE CASCADE,
  enrolled_on DATE DEFAULT (CURRENT_DATE),
  PRIMARY KEY (athlete_id, sport_id)
);