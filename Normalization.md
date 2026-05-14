# Normalization Walkthrough

**Project:** AthleteIQ
**Milestone 2**   

---

## Tables in Schema

- ATHLETES
- SPORTS
- USERS
- ATHLETE_ENROLLMENTS
- INJURY_RECORDS
- PERFORMANCE_STATS

---

## First Normal Form (1NF)


All six tables satisfy 1NF. Every column across all tables holds atomic, single values with no repeating groups or multi-valued attributes. Each table has a defined primary key — `athlete_id`, `sport_id`, `user_id`, `injury_id`, `stat_id`, and a composite `(athlete_id, sport_id)` in ATHLETE_ENROLLMENTS.

**Result:** No changes were needed.

---

## Second Normal Form (2NF)


Five of the six tables have single-column primary keys, making partial dependencies impossible by definition. The only composite key exists in ATHLETE_ENROLLMENTS, where the sole non-key attribute `enrolled_on` depends on both `athlete_id` and `sport_id` together — representing the date a specific athlete enrolled in a specific sport. No partial dependency exists.

**Result:** No changes were needed.

---

## Third Normal Form (3NF)


### ATHLETES
All attributes (`full_name`, `date_of_birth`, `gender`, `nationality`, `contact`, `status`, `created_at`) describe the athlete directly and depend solely on `athlete_id`. No transitive dependencies exist.

### SPORTS
Both `name` and `category` depend directly on `sport_id`. `category` is a simple descriptive field with no attributes of its own, so no transitive dependency arises.

### USERS
`username`, `password_hash`, and `created_at` all depend directly on `user_id`. No attribute is derived from another non-key column.

### ATHLETE_ENROLLMENTS
The only non-key attribute is `enrolled_on`, which depends directly on the composite key `(athlete_id, sport_id)`. No transitive dependency is possible.

### INJURY_RECORDS
All attributes (`injury_type`, `severity`, `date_occured`, `recovery_status`, `notes`) describe the specific injury instance and depend directly on `injury_id`. No transitive dependency is possible.

### PERFORMANCE_STATS
`metric_name`, `value`, and `recorded_on` all depend directly on `stat_id`. `athlete_id` and `sport_id` appear as foreign keys, not as sources of transitive dependency.

**Result:** No changes were needed across any table.

---

## Redundancy Check

No redundant or overlapping columns were found. Each table serves a distinct purpose:

| Table | Purpose |
|---|---|
| ATHLETES | Stores athlete identity and personal information |
| SPORTS | Stores sport definitions and categories |
| USERS | Stores system account credentials |
| ATHLETE_ENROLLMENTS | Records which athletes participate in which sports |
| INJURY_RECORDS | Logs medical/injury incidents per athlete |
| PERFORMANCE_STATS | Tracks measurable performance metrics per athlete per sport |


---

## Summary

| Normal Form | Status | Changes Made |
|---|---|---|
| 1NF | Satisfied | None |
| 2NF | Satisfied | None |
| 3NF | Satisfied | None |

The schema was already fully normalized to 3NF as designed.