USE athleteiq;

CREATE TABLE athletes (
  athlete_id   SERIAL      PRIMARY KEY,
  full_name    VARCHAR(120) NOT NULL,
  date_of_birth DATE       NOT NULL,
  gender       VARCHAR(20),
  nationality  VARCHAR(80),
  contact_info TEXT,
  status       VARCHAR(20) NOT NULL DEFAULT 'active'
                             CHECK (status IN ('active', 'inactive', 'retired')),
  created_at   TIMESTAMP DEFAULT now()
);