"""
AthleteIQ - Synthetic Data Generator
Generates realistic CSV data for all 6 tables.
Requirements: pip install faker
Run: python generate_data.py
"""

import csv
import random
import hashlib
from datetime import date, timedelta
from faker import Faker

fake = Faker()
random.seed(42)

OUTPUT_DIR = "./"  # Change this to your preferred output folder

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def random_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, (end - start).days))

def fake_password_hash(username: str) -> str:
    return hashlib.sha256(f"{username}_athleteiq".encode()).hexdigest()

def write_csv(filename: str, fieldnames: list, rows: list):
    path = OUTPUT_DIR + filename
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  [OK] {filename} — {len(rows)} rows")


# ─────────────────────────────────────────────
# 1. SPORTS
# ─────────────────────────────────────────────
# Small reference table — fixed realistic entries for AthleteIQ

SPORTS_DATA = [
    {"sport_id": 1, "name": "Football",        "category": "Team Sport"},
    {"sport_id": 2, "name": "Futsal",          "category": "Team Sport"},
    {"sport_id": 3, "name": "Basketball",      "category": "Team Sport"},
    {"sport_id": 4, "name": "Swimming",        "category": "Individual Sport"},
    {"sport_id": 5, "name": "Athletics",       "category": "Individual Sport"},
    {"sport_id": 6, "name": "Badminton",       "category": "Racket Sport"},
    {"sport_id": 7, "name": "Volleyball",      "category": "Team Sport"},
    {"sport_id": 8, "name": "Table Tennis",    "category": "Racket Sport"},
]
sport_ids = [s["sport_id"] for s in SPORTS_DATA]

write_csv("sports.csv", ["sport_id", "name", "category"], SPORTS_DATA)


# ─────────────────────────────────────────────
# 2. USERS
# Represents application admin accounts — individuals who log into
# the AthleteIQ system to manage athletes, sports, and records.
# ─────────────────────────────────────────────

users = []
for i in range(1, 81):
    username = fake.unique.user_name()
    users.append({
        "user_id":       i,
        "username":      username,
        "password_hash": fake_password_hash(username),
        "created_at":    fake.date_time_between(start_date="-3y", end_date="now").isoformat(),
    })

write_csv("users.csv", ["user_id", "username", "password_hash", "created_at"], users)


# ─────────────────────────────────────────────
# 3. ATHLETES
# ─────────────────────────────────────────────

NATIONALITIES = [
    "Pakistani", "Brazilian", "Spanish", "German", "French",
    "Argentine", "English", "Nigerian", "Japanese", "American",
    "Dutch", "Portuguese", "Italian", "Moroccan", "South Korean"
]

STATUSES = ["active", "active", "active", "inactive", "retired"]  # weighted toward active

athletes = []
for i in range(1, 101):
    gender = random.choice(["Male", "Female"])
    athletes.append({
        "athlete_id":   i,
        "full_name":    fake.name_male() if gender == "Male" else fake.name_female(),
        "date_of_birth": random_date(date(1995, 1, 1), date(2005, 12, 31)).isoformat(),
        "gender":       gender,
        "nationality":  random.choice(NATIONALITIES),
        "contact_info": fake.phone_number(),
        "status":       random.choice(STATUSES),
        "created_at":   fake.date_time_between(start_date="-3y", end_date="now").isoformat(),
    })

athlete_ids = [a["athlete_id"] for a in athletes]
write_csv("athletes.csv",
          ["athlete_id", "full_name", "date_of_birth", "gender", "nationality", "contact_info", "status", "created_at"],
          athletes)


# ─────────────────────────────────────────────
# 4. ATHLETE_ENROLLMENTS
# ─────────────────────────────────────────────
# Each athlete enrolls in 1-3 sports. No duplicate (athlete_id, sport_id) pairs.

enrollments = []
enrollment_pairs = set()  # track composite PK uniqueness

for athlete_id in athlete_ids:
    num_sports = random.randint(1, 3)
    chosen_sports = random.sample(sport_ids, num_sports)
    for sport_id in chosen_sports:
        pair = (athlete_id, sport_id)
        if pair not in enrollment_pairs:
            enrollment_pairs.add(pair)
            enrollments.append({
                "athlete_id":  athlete_id,
                "sport_id":    sport_id,
                "enrolled_on": random_date(date(2022, 1, 1), date(2024, 6, 30)).isoformat(),
            })

write_csv("athlete_enrollments.csv", ["athlete_id", "sport_id", "enrolled_on"], enrollments)

# Build a lookup: which sport(s) each athlete is enrolled in
athlete_sports = {}
for e in enrollments:
    athlete_sports.setdefault(e["athlete_id"], []).append(e["sport_id"])


# ─────────────────────────────────────────────
# 5. INJURY_RECORDS
# ─────────────────────────────────────────────

INJURY_TYPES = [
    "Hamstring Strain", "ACL Tear", "Knee Sprain", "Ankle Sprain",
    "Shoulder Dislocation", "Muscle Fatigue", "Shin Splints",
    "Concussion", "Groin Strain", "Lower Back Pain"
]
SEVERITIES        = ["mild", "moderate", "severe"]
RECOVERY_STATUSES = ["ongoing", "recovered", "chronic"]

injury_records = []
for i in range(1, 81):
    athlete_id = random.choice(athlete_ids)
    injury_records.append({
        "injury_id":       i,
        "athlete_id":      athlete_id,
        "injury_type":     random.choice(INJURY_TYPES),
        "severity":        random.choice(SEVERITIES),
        "date_occurred":   random_date(date(2022, 1, 1), date(2024, 12, 31)).isoformat(),
        "recovery_status": random.choice(RECOVERY_STATUSES),
        "notes":           fake.sentence(nb_words=12),
    })

write_csv("injury_records.csv",
          ["injury_id", "athlete_id", "injury_type", "severity", "date_occurred", "recovery_status", "notes"],
          injury_records)


# ─────────────────────────────────────────────
# 6. PERFORMANCE_STATS
# ─────────────────────────────────────────────
# Metrics are sport-specific and realistic for AthleteIQ's focus on Football/Futsal

SPORT_METRICS = {
    1: ["Goals Scored", "Assists", "Pass Accuracy (%)", "Distance Covered (km)", "Shot Accuracy (%)"],  # Football
    2: ["Goals Scored", "Assists", "Pass Accuracy (%)", "Sprint Speed (km/h)", "Tackles Won"],           # Futsal
    3: ["Points Scored", "Rebounds", "Assists", "Field Goal % "],                                        # Basketball
    4: ["Lap Time (s)", "Distance (m)", "Stroke Rate"],                                                  # Swimming
    5: ["100m Time (s)", "Long Jump (m)", "High Jump (m)"],                                              # Athletics
    6: ["Smash Speed (km/h)", "Rally Length", "Service Accuracy (%)"],                                   # Badminton
    7: ["Kills", "Blocks", "Service Aces", "Dig Success (%)"],                                          # Volleyball
    8: ["Points Won", "Serve Accuracy (%)", "Rally Win Rate (%)"],                                       # Table Tennis
}

METRIC_RANGES = {
    "Goals Scored":           (0, 15),
    "Assists":                (0, 20),
    "Pass Accuracy (%)":      (55, 98),
    "Distance Covered (km)":  (6.0, 13.0),
    "Shot Accuracy (%)":      (20, 80),
    "Sprint Speed (km/h)":    (22, 36),
    "Tackles Won":            (0, 30),
    "Points Scored":          (5, 40),
    "Rebounds":               (2, 20),
    "Field Goal % ":          (30, 65),
    "Lap Time (s)":           (50, 120),
    "Distance (m)":           (50, 1500),
    "Stroke Rate":            (25, 60),
    "100m Time (s)":          (10, 14),
    "Long Jump (m)":          (4, 9),
    "High Jump (m)":          (1.5, 2.5),
    "Smash Speed (km/h)":     (150, 320),
    "Rally Length":           (3, 30),
    "Service Accuracy (%)":   (40, 90),
    "Kills":                  (3, 25),
    "Blocks":                 (0, 15),
    "Service Aces":           (0, 10),
    "Dig Success (%)":        (50, 95),
    "Points Won":             (5, 30),
    "Serve Accuracy (%)":     (50, 90),
    "Rally Win Rate (%)":     (40, 75),
}

def get_value(metric: str) -> float:
    low, high = METRIC_RANGES.get(metric, (0, 100))
    if isinstance(low, float) or isinstance(high, float):
        return round(random.uniform(low, high), 3)
    return round(random.uniform(low, high), 3)

performance_stats = []
stat_id = 1

for athlete_id, sports in athlete_sports.items():
    for sport_id in sports:
        metrics = SPORT_METRICS.get(sport_id, ["General Score"])
        num_entries = random.randint(2, 4)  # multiple recorded sessions per athlete per sport
        for _ in range(num_entries):
            metric = random.choice(metrics)
            performance_stats.append({
                "stat_id":     stat_id,
                "athlete_id":  athlete_id,
                "sport_id":    sport_id,
                "metric_name": metric,
                "value":       get_value(metric),
                "recorded_on": random_date(date(2022, 6, 1), date(2024, 12, 31)).isoformat(),
            })
            stat_id += 1

write_csv("performance_stats.csv",
          ["stat_id", "athlete_id", "sport_id", "metric_name", "value", "recorded_on"],
          performance_stats)


# ─────────────────────────────────────────────
# DONE
# ─────────────────────────────────────────────
print("\nAll CSV files generated successfully.")
print(f"  sports.csv              — {len(SPORTS_DATA)} rows")
print(f"  users.csv               — {len(users)} rows")
print(f"  athletes.csv            — {len(athletes)} rows")
print(f"  athlete_enrollments.csv — {len(enrollments)} rows")
print(f"  injury_records.csv      — {len(injury_records)} rows")
print(f"  performance_stats.csv   — {len(performance_stats)} rows")
