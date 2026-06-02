# AthleteIQ: Multi-Sport Athlete Database Management System

AthleteIQ is a relational database project for managing athlete profiles, sport enrollments, injuries, and performance statistics across multiple sports.

This repository now includes schema design, normalization/dataflow documentation, DDL and DML SQL scripts, population datasets, and validation evidence.

## Project Information
- **Institution:** Institute of Management Sciences, Peshawar  
- **Department:** School of Computer Sciences & IT  
- **Lab Instructor:** Mr. Ali Hasan

## Project Team
- Ismail Khan
- Rayan Alam

---

## 🛠 Database Schema
The system contains six core tables:

1. **athletes**  
   `athlete_id` (PK), `full_name`, `date_of_birth`, `gender`, `nationality`, `contact_info`, `status`, `created_at`

2. **sports**  
   `sport_id` (PK), `name`, `category`

3. **athlete_enrollments**  
   `athlete_id` (FK), `sport_id` (FK), `enrolled_on`  
   Composite PK: (`athlete_id`, `sport_id`)

4. **injury_records**  
   `injury_id` (PK), `athlete_id` (FK), `injury_type`, `severity`, `date_occurred`, `recovery_status`, `notes`

5. **performance_stats**  
   `stat_id` (PK), `athlete_id` (FK), `sport_id` (FK), `metric_name`, `value`, `recorded_on`

6. **users**  
   `user_id` (PK), `username`, `password_hash`, `created_at`

---

## 📁 Repository Structure

### Core documentation
- `Dataflow.md` — end-to-end system dataflow and load-order explanation
- `Normalization.md` — 1NF/2NF/3NF walkthrough
- `EER_Diagram.png`, `ERD.drawio.png`, `ERD.drawio.html` — ERD/EER assets

### SQL scripts
- `DDL_Scripts/`  
  Table creation scripts and indexes:
  - `athlete_users.sql`
  - `athlete_sports.sql`
  - `athlete_athletes.sql`
  - `athlete_enrollments.sql`
  - `athlete_injury.sql`
  - `athlete_performance.sql`
  - `athlete_indexes.sql`

- `DML_Scripts/`
  - `population_script.sql` — bulk CSV loading
  - `DML_operations.sql` — sample update/delete operations
  - `DML_validation.sql` — row-count, null, and FK integrity checks

### Data assets
- `Population_data/` — CSV datasets used for bulk load
- `generate_data.py` — Python script to regenerate synthetic CSV data (requires `faker`)

### Output evidence
- `Outputs_Screenshots/` — query/validation screenshots (row counts, null checks, FK integrity)

---

## ▶️ Typical Execution Flow
1. Create database and tables using scripts in `DDL_Scripts/`.
2. Load CSV data with `DML_Scripts/population_script.sql`.
3. Run `DML_Scripts/DML_operations.sql` for sample DML changes.
4. Run `DML_Scripts/DML_validation.sql` to verify integrity.

---

## 📅 Project Milestones
| Milestones | Version | Date | Remarks |
| :--- | :--- | :--- | :--- |
| 1. Created Schema and Designed ERD | V 1.0 | 23/4/26 |  |
| 2. Normalization and redundancy checks | V 1.1 | 12/5/26 |  |
| 3. Generated synthetic data and Defined data flow | V 1.2 | 14/5/26 |  |
| 4. DDL scripts implemented and EERD verified | V 1.3 | 14/5/26 |  |
| 5. Data population and screenshots taken | V 1.4 | 15/5/26 |  |
