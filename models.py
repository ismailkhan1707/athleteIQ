import hashlib
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


# ── Users ────────────────────────────────────────────────────────────────────
class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # Flask-Login requires an `id` property
    def get_id(self):
        return str(self.user_id)

    def check_password(self, password):
        """SHA-256 comparison using username_athleteiq salt convention."""
        expected = hashlib.sha256(
            f"{self.username}_athleteiq".encode()
        ).hexdigest()
        return self.password_hash == expected


# ── Athletes ─────────────────────────────────────────────────────────────────
class Athlete(db.Model):
    __tablename__ = "athletes"

    athlete_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    nationality = db.Column(db.String(80))
    contact_info = db.Column(db.Text)
    status = db.Column(db.String(20))  # CHECK in DB: active / inactive / retired
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # relationships
    enrollments = db.relationship(
        "AthleteEnrollment", back_populates="athlete", lazy="dynamic"
    )
    injuries = db.relationship(
        "InjuryRecord", back_populates="athlete", lazy="dynamic"
    )
    performance_stats = db.relationship(
        "PerformanceStat", back_populates="athlete", lazy="dynamic"
    )


# ── Sports ───────────────────────────────────────────────────────────────────
class Sport(db.Model):
    __tablename__ = "sports"

    sport_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(60))

    # relationships
    enrollments = db.relationship(
        "AthleteEnrollment", back_populates="sport", lazy="dynamic"
    )
    performance_stats = db.relationship(
        "PerformanceStat", back_populates="sport", lazy="dynamic"
    )


# ── Athlete Enrollments (composite PK) ──────────────────────────────────────
class AthleteEnrollment(db.Model):
    __tablename__ = "athlete_enrollments"

    athlete_id = db.Column(
        db.Integer, db.ForeignKey("athletes.athlete_id"), primary_key=True
    )
    sport_id = db.Column(
        db.Integer, db.ForeignKey("sports.sport_id"), primary_key=True
    )
    enrolled_on = db.Column(db.Date)

    # relationships
    athlete = db.relationship("Athlete", back_populates="enrollments")
    sport = db.relationship("Sport", back_populates="enrollments")


# ── Injury Records ──────────────────────────────────────────────────────────
class InjuryRecord(db.Model):
    __tablename__ = "injury_records"

    injury_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    athlete_id = db.Column(
        db.Integer, db.ForeignKey("athletes.athlete_id"), nullable=False
    )
    injury_type = db.Column(db.String(100))
    severity = db.Column(db.String(20))       # CHECK: mild / moderate / severe
    date_occurred = db.Column(db.Date)
    recovery_status = db.Column(db.String(30))  # CHECK: ongoing / recovered / chronic
    notes = db.Column(db.Text)

    # relationship
    athlete = db.relationship("Athlete", back_populates="injuries")


# ── Performance Stats ───────────────────────────────────────────────────────
class PerformanceStat(db.Model):
    __tablename__ = "performance_stats"

    stat_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    athlete_id = db.Column(
        db.Integer, db.ForeignKey("athletes.athlete_id"), nullable=False
    )
    sport_id = db.Column(
        db.Integer, db.ForeignKey("sports.sport_id"), nullable=False
    )
    metric_name = db.Column(db.String(80))
    value = db.Column(db.Numeric(10, 3))
    recorded_on = db.Column(db.Date)

    # relationships
    athlete = db.relationship("Athlete", back_populates="performance_stats")
    sport = db.relationship("Sport", back_populates="performance_stats")
