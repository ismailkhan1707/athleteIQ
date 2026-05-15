CREATE DATABASE IF NOT EXISTS athleteIQ;

USE athleteIQ;

CREATE TABLE users(
	user_id SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);