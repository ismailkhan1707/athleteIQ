# AthleteIQ: Multi-Sport Athlete Database Management System

AthleteIQ is a comprehensive database management system designed to track personal details, enrollment, performance metrics, and medical history for athletes across various sports disciplines. This project was developed as part of the Database Lab curriculum at the Institute of Management Sciences, Peshawar.

## Project Information
* **Institution:** Institute of Management Sciences, Peshawar
* **Department:** School of Computer Sciences & IT
* **Lab Instructor:** Mr. Ali Hasan

## Project Team
* Ismail Khan
* Rayan Alam

---

## 🛠 Database Schema
The system consists of six core tables to manage the ecosystem of athletes, sports, and administrative users.

### 1. Athletes
Stores personal profile information.
* **Attributes:** `athlete_id` (PK), `full_name`, `date_of_birth`, `gender`, `nationality`, `contact_info`, `status`, `created_at`.

### 2. Sports
A catalog of available sports and categories.
* **Attributes:** `sport_id`, `name`, `category`.

### 3. Athlete Enrollments
Records which athletes are enrolled in what sport and when.
* **Attributes:** `athlete_id` (FK), `sport_id` (FK), `enrolled_on`.

### 4. Injury Records
Maintains a history of injuries, severity, and recovery status.
* **Attributes:** `injury_id` (PK), `athlete_id` (FK), `injury_type`, `severity`, `date_occured`, `recovery_status`, `notes`.

### 5. Performance Stats
Logs measurable performance metrics for athletes across sports over time.
* **Attributes:** `stat_id` (PK), `athlete_id` (FK), `sport_id` (FK), `metric_name`, `value`, `recorded_on`.

### 6. Users
Manages system login credentials for admins, coaches, or staff.
* **Attributes:** `user_id` (PK), `username`, `password_hash`, `created_at`.

---

## 📊 Entity Relationship Diagram (ERD)
The database structure establishes clear relationships between athletes, their sports enrollments, performance tracking, and medical history.

---

## 📅 Project Milestones
| Milestones | Version | Date | Remarks |
| :--- | :--- | :--- | :--- |
| Created Schema and Designed ERD | V 1.0 | 23/4/26 | Initial Design |
