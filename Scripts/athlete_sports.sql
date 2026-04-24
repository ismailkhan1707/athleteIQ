USE athleteiq;

CREATE TABLE sports (
  sport_id   SERIAL      PRIMARY KEY,
  name       VARCHAR(80) NOT NULL UNIQUE,
  category   VARCHAR(60)
);