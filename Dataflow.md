# AthleteIQ — Dataflow Description

## Overview

AthleteIQ is a multi-sport athlete management system that tracks athlete registrations, sport enrollments, injury history, and performance statistics across multiple sports such as Football and Futsal. Data flows from administrative input and coaching staff through a structured relational database, and is queried to produce reports, performance summaries, and health monitoring outputs.

---

## Data Entry Points

Data enters the AthleteIQ system through the following sources:

- **Admin Login** — USERS represents application-level admin accounts. These are individuals who log into the AthleteIQ system using their credentials to manage athletes, sports, enrollments, and records. They are not coaches or managers but system administrators with access to the application interface.
- **Athlete Registration** — When a new athlete joins the system, their personal information (name, date of birth, gender, nationality, contact, status) is recorded in the ATHLETES table.
- **Sport Enrollment** — Coaching staff enroll athletes into specific sports, creating records in ATHLETE_ENROLLMENTS that link an athlete to a sport with an enrollment date.
- **Injury Reporting** — Medical staff or coaches log injury incidents for athletes, writing to the INJURY_RECORDS table with details on injury type, severity, date, and recovery status.
- **Performance Logging** — After training sessions or matches, coaches or analysts record performance metrics (goals scored, pass accuracy, sprint speed, etc.) for each athlete per sport, writing to the PERFORMANCE_STATS table.

---

## Data Flow Through the Database

The tables have a clear dependency order that data must respect:

```
USERS
    (independent — application admin accounts for system login)

SPORTS
    (independent — reference table of available sports)

ATHLETES
    (independent — registered athletes)

ATHLETE_ENROLLMENTS
    depends on → ATHLETES (athlete_id)
    depends on → SPORTS   (sport_id)

INJURY_RECORDS
    depends on → ATHLETES (athlete_id)

PERFORMANCE_STATS
    depends on → ATHLETES (athlete_id)
    depends on → SPORTS   (sport_id)
```

**Load order for data population:**
SPORTS and ATHLETES must be populated before ATHLETE_ENROLLMENTS, INJURY_RECORDS, or PERFORMANCE_STATS can reference them. USERS is independent and can be loaded at any point.

---

## Data Outputs

Once data is loaded, the system supports the following query outputs:

- **Athlete Profile Report** — Joins ATHLETES with ATHLETE_ENROLLMENTS and SPORTS to show which sports an athlete is enrolled in.
- **Performance Summary** — Queries PERFORMANCE_STATS filtered by athlete_id and sport_id to return recorded metrics over time (e.g., goal scoring trend across football sessions).
- **Injury History Report** — Queries INJURY_RECORDS by athlete_id to display a timeline of injuries, severity levels, and recovery status for medical staff review.
- **Sport Roster** — Joins ATHLETE_ENROLLMENTS with ATHLETES to list all athletes enrolled in a given sport (e.g., all Football players).
- **Active vs Inactive Athletes** — Filters ATHLETES by status to monitor which athletes are currently active in the system.
