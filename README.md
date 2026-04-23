# AthleteIQ: Multi-Sport Athlete Database Management System

AthleteIQ is a comprehensive database management system designed to track personal details, enrollment, performance metrics, and medical history for athletes across various sports disciplines. [cite_start]This project was developed as part of the Database Lab curriculum. [cite: 1, 2, 3]

## Project Information
* [cite_start]**Project Name:** AthleteIQ [cite: 1]
* [cite_start]**Institution:** Institute of Management Sciences, Peshawar [cite: 13]
* [cite_start]**Department:** School of Computer Sciences & IT [cite: 12]
* [cite_start]**Lab Instructor:** Mr. Ali Hasan [cite: 7, 11]

## Project Team
* [cite_start]Ismail Khan [cite: 5, 9]
* [cite_start]Rayan Alam [cite: 6, 10]

---

## 🛠 Database Schema
[cite_start]The system consists of six core tables to manage the ecosystem of athletes, sports, and administrative users. [cite: 15]

### 1. Athletes
[cite_start]Stores personal profile information. [cite: 17]
* [cite_start]**Key Fields:** `athlete_id` (PK), `full_name`, `date_of_birth`, `nationality`, `status`. [cite: 19, 20, 21, 23, 25]

### 2. Sports
[cite_start]A catalog of available sports and categories. [cite: 28]
* [cite_start]**Key Fields:** `sport_id` (PK), `name`, `category`. [cite: 30, 31, 32]

### 3. Athlete Enrollments
[cite_start]Tracks which athletes are enrolled in specific sports and their start dates. [cite: 34]
* [cite_start]**Key Fields:** `athlete_id` (FK), `sport_id` (FK), `enrolled_on`. [cite: 36, 37, 38]

### 4. Injury Records
[cite_start]Maintains a history of injuries, severity, and recovery progress. [cite: 40]
* [cite_start]**Key Fields:** `injury_id` (PK), `athlete_id` (FK), `injury_type`, `severity`, `recovery_status`. [cite: 42, 43, 44, 45, 47]

### 5. Performance Stats
[cite_start]Logs measurable performance metrics (e.g., speed, score) over time. [cite: 50]
* [cite_start]**Key Fields:** `stat_id` (PK), `athlete_id` (FK), `sport_id` (FK), `metric_name`, `value`. [cite: 52, 53, 54, 55, 56]

### 6. Users
[cite_start]Management of login credentials for system administrators and coaches. [cite: 59]
* [cite_start]**Key Fields:** `user_id` (PK), `username`, `password_hash`. [cite: 61, 62, 63]

---

## 📊 Entity Relationship Diagram (ERD)
[cite_start]The database follows a relational structure where the `Athletes` and `Sports` tables serve as the primary entities, linked through enrollment and performance tracking tables. [cite: 65]


---

## 📅 Project Milestones
| Milestone | Version | Date | Remarks |
| :--- | :--- | :--- | :--- |
| Created Schema and Designed ERD | V 1.0 | 23/04/2026 | [cite_start]Initial Release [cite: 14] |
