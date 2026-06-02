import json
from datetime import date

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from sqlalchemy import func

from config import Config
from models import (
    db,
    User,
    Athlete,
    Sport,
    AthleteEnrollment,
    InjuryRecord,
    PerformanceStat,
)

# ─── App factory ─────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ═══════════════════════════════════════════════════════════════════════════════
#  AUTH
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ═══════════════════════════════════════════════════════════════════════════════
#  USER MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/users")
@login_required
def users_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("users/list.html", users=users)


@app.route("/users/add", methods=["GET", "POST"])
@login_required
def user_add():
    if request.method == "POST":
        import hashlib

        username = request.form.get("username", "").strip()
        if not username:
            flash("Username is required.", "danger")
            return render_template("users/form.html")

        # Check if username already exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            flash("Username already exists.", "danger")
            return render_template("users/form.html")

        # Generate password hash using the project convention
        password_hash = hashlib.sha256(
            f"{username}_athleteiq".encode()
        ).hexdigest()

        user = User(username=username, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        flash(f"User '{username}' created successfully.", "success")
        return redirect(url_for("users_list"))

    return render_template("users/form.html")


@app.route("/users/<int:id>/delete", methods=["POST"])
@login_required
def user_delete(id):
    user = db.session.get(User, id)
    if not user:
        flash("User not found.", "danger")
    elif user.user_id == current_user.user_id:
        flash("You cannot delete your own account.", "warning")
    else:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully.", "success")
    return redirect(url_for("users_list"))


# ═══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/")
@login_required
def dashboard():
    # ── scalar counts ────────────────────────────────────────────────────────
    total_athletes = db.session.query(func.count(Athlete.athlete_id)).scalar() or 0
    active_athletes = (
        db.session.query(func.count(Athlete.athlete_id))
        .filter(Athlete.status == "active")
        .scalar()
        or 0
    )
    total_sports = db.session.query(func.count(Sport.sport_id)).scalar() or 0
    total_injuries = db.session.query(func.count(InjuryRecord.injury_id)).scalar() or 0
    total_performance = (
        db.session.query(func.count(PerformanceStat.stat_id)).scalar() or 0
    )

    # ── nationality breakdown ────────────────────────────────────────────────
    nat_rows = (
        db.session.query(Athlete.nationality, func.count(Athlete.athlete_id))
        .group_by(Athlete.nationality)
        .all()
    )
    nationality_labels = json.dumps([r[0] or "Unknown" for r in nat_rows])
    nationality_data = json.dumps([r[1] for r in nat_rows])

    # ── injury severity breakdown ────────────────────────────────────────────
    sev_order = ["mild", "moderate", "severe"]
    sev_counts = {}
    sev_rows = (
        db.session.query(InjuryRecord.severity, func.count(InjuryRecord.injury_id))
        .group_by(InjuryRecord.severity)
        .all()
    )
    for label, cnt in sev_rows:
        sev_counts[label] = cnt
    severity_labels = json.dumps(sev_order)
    severity_data = json.dumps([sev_counts.get(s, 0) for s in sev_order])

    # ── sport enrollment counts ──────────────────────────────────────────────
    sport_rows = (
        db.session.query(Sport.name, func.count(AthleteEnrollment.athlete_id))
        .outerjoin(AthleteEnrollment, Sport.sport_id == AthleteEnrollment.sport_id)
        .group_by(Sport.name)
        .all()
    )
    sport_labels = json.dumps([r[0] for r in sport_rows])
    sport_data = json.dumps([r[1] for r in sport_rows])

    # ── recent athletes ──────────────────────────────────────────────────────
    recent_athletes = (
        Athlete.query.order_by(Athlete.created_at.desc()).limit(5).all()
    )

    return render_template(
        "dashboard.html",
        total_athletes=total_athletes,
        active_athletes=active_athletes,
        total_sports=total_sports,
        total_injuries=total_injuries,
        total_performance=total_performance,
        nationality_labels=nationality_labels,
        nationality_data=nationality_data,
        severity_labels=severity_labels,
        severity_data=severity_data,
        sport_labels=sport_labels,
        sport_data=sport_data,
        recent_athletes=recent_athletes,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  ATHLETES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/athletes")
@login_required
def athletes_list():
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()

    query = Athlete.query
    if search:
        if search.isdigit():
            query = query.filter(
                db.or_(Athlete.athlete_id == int(search),
                       Athlete.full_name.ilike(f"%{search}%"))
            )
        else:
            query = query.filter(Athlete.full_name.ilike(f"%{search}%"))
    if status:
        query = query.filter(Athlete.status == status)

    athletes = query.order_by(Athlete.full_name).all()
    return render_template(
        "athletes/list.html", athletes=athletes, search=search, status=status
    )


@app.route("/athletes/<int:id>")
@login_required
def athlete_detail(id):
    athlete = db.session.get(Athlete, id)
    if not athlete:
        flash("Athlete not found.", "danger")
        return redirect(url_for("athletes_list"))

    # eager‑load related data
    enrollments = athlete.enrollments.all()
    injuries = athlete.injuries.all()
    stats = athlete.performance_stats.all()

    return render_template(
        "athletes/detail.html",
        athlete=athlete,
        enrollments=enrollments,
        injuries=injuries,
        stats=stats,
    )


@app.route("/athletes/add", methods=["GET", "POST"])
@login_required
def athlete_add():
    sports = Sport.query.order_by(Sport.name).all()

    if request.method == "POST":
        athlete = Athlete(
            full_name=request.form.get("full_name", "").strip(),
            date_of_birth=request.form.get("date_of_birth") or None,
            gender=request.form.get("gender", "").strip() or None,
            nationality=request.form.get("nationality", "").strip() or None,
            contact_info=request.form.get("contact_info", "").strip() or None,
            status=request.form.get("status", "active"),
        )
        db.session.add(athlete)
        db.session.commit()
        flash("Athlete added successfully.", "success")
        return redirect(url_for("athletes_list"))

    return render_template("athletes/form.html", athlete=None, sports=sports)


@app.route("/athletes/<int:id>/edit", methods=["GET", "POST"])
@login_required
def athlete_edit(id):
    athlete = db.session.get(Athlete, id)
    if not athlete:
        flash("Athlete not found.", "danger")
        return redirect(url_for("athletes_list"))

    sports = Sport.query.order_by(Sport.name).all()

    if request.method == "POST":
        athlete.full_name = request.form.get("full_name", "").strip()
        athlete.date_of_birth = request.form.get("date_of_birth") or None
        athlete.gender = request.form.get("gender", "").strip() or None
        athlete.nationality = request.form.get("nationality", "").strip() or None
        athlete.contact_info = request.form.get("contact_info", "").strip() or None
        athlete.status = request.form.get("status", "active")
        db.session.commit()
        flash("Athlete updated successfully.", "success")
        return redirect(url_for("athletes_list"))

    return render_template("athletes/form.html", athlete=athlete, sports=sports)


@app.route("/athletes/<int:id>/delete", methods=["POST"])
@login_required
def athlete_delete(id):
    athlete = db.session.get(Athlete, id)
    if not athlete:
        flash("Athlete not found.", "danger")
    else:
        db.session.delete(athlete)
        db.session.commit()
        flash("Athlete deleted successfully.", "success")
    return redirect(url_for("athletes_list"))


# ═══════════════════════════════════════════════════════════════════════════════
#  SPORTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/sports")
@login_required
def sports_list():
    search = request.args.get("search", "").strip()
    query = Sport.query
    if search:
        if search.isdigit():
            query = query.filter(
                db.or_(Sport.sport_id == int(search),
                       Sport.name.ilike(f"%{search}%"))
            )
        else:
            query = query.filter(Sport.name.ilike(f"%{search}%"))
    sports = query.order_by(Sport.name).all()
    return render_template("sports/list.html", sports=sports, search=search)


@app.route("/sports/add", methods=["GET", "POST"])
@login_required
def sport_add():
    if request.method == "POST":
        sport = Sport(
            name=request.form.get("name", "").strip(),
            category=request.form.get("category", "").strip() or None,
        )
        db.session.add(sport)
        db.session.commit()
        flash("Sport added successfully.", "success")
        return redirect(url_for("sports_list"))

    return render_template("sports/form.html", sport=None)


@app.route("/sports/<int:id>/edit", methods=["GET", "POST"])
@login_required
def sport_edit(id):
    sport = db.session.get(Sport, id)
    if not sport:
        flash("Sport not found.", "danger")
        return redirect(url_for("sports_list"))

    if request.method == "POST":
        sport.name = request.form.get("name", "").strip()
        sport.category = request.form.get("category", "").strip() or None
        db.session.commit()
        flash("Sport updated successfully.", "success")
        return redirect(url_for("sports_list"))

    return render_template("sports/form.html", sport=sport)


@app.route("/sports/<int:id>/delete", methods=["POST"])
@login_required
def sport_delete(id):
    sport = db.session.get(Sport, id)
    if not sport:
        flash("Sport not found.", "danger")
    else:
        db.session.delete(sport)
        db.session.commit()
        flash("Sport deleted successfully.", "success")
    return redirect(url_for("sports_list"))


# ═══════════════════════════════════════════════════════════════════════════════
#  ENROLLMENTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/enrollments")
@login_required
def enrollments_list():
    search = request.args.get("search", "").strip()
    query = (
        AthleteEnrollment.query
        .join(Athlete, AthleteEnrollment.athlete_id == Athlete.athlete_id)
        .join(Sport, AthleteEnrollment.sport_id == Sport.sport_id)
    )
    if search:
        if search.isdigit():
            query = query.filter(
                db.or_(AthleteEnrollment.athlete_id == int(search),
                       AthleteEnrollment.sport_id == int(search),
                       Athlete.full_name.ilike(f"%{search}%"),
                       Sport.name.ilike(f"%{search}%"))
            )
        else:
            query = query.filter(
                db.or_(Athlete.full_name.ilike(f"%{search}%"),
                       Sport.name.ilike(f"%{search}%"))
            )
    enrollments = query.order_by(Athlete.full_name).all()
    athletes = Athlete.query.order_by(Athlete.full_name).all()
    sports = Sport.query.order_by(Sport.name).all()
    return render_template(
        "enrollments/list.html",
        enrollments=enrollments,
        athletes=athletes,
        sports=sports,
        search=search,
    )


@app.route("/enrollments/add", methods=["POST"])
@login_required
def enrollment_add():
    athlete_id = request.form.get("athlete_id", type=int)
    sport_id = request.form.get("sport_id", type=int)
    enrolled_on = request.form.get("enrolled_on") or date.today().isoformat()

    # check for duplicates
    existing = db.session.get(AthleteEnrollment, (athlete_id, sport_id))
    if existing:
        flash("This athlete is already enrolled in that sport.", "warning")
    else:
        enrollment = AthleteEnrollment(
            athlete_id=athlete_id,
            sport_id=sport_id,
            enrolled_on=enrolled_on,
        )
        db.session.add(enrollment)
        db.session.commit()
        flash("Enrollment added successfully.", "success")

    return redirect(url_for("enrollments_list"))


@app.route("/enrollments/delete", methods=["POST"])
@login_required
def enrollment_delete():
    athlete_id = request.form.get("athlete_id", type=int)
    sport_id = request.form.get("sport_id", type=int)

    enrollment = db.session.get(AthleteEnrollment, (athlete_id, sport_id))
    if not enrollment:
        flash("Enrollment not found.", "danger")
    else:
        db.session.delete(enrollment)
        db.session.commit()
        flash("Enrollment deleted successfully.", "success")

    return redirect(url_for("enrollments_list"))


# ═══════════════════════════════════════════════════════════════════════════════
#  INJURIES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/injuries")
@login_required
def injuries_list():
    search = request.args.get("search", "").strip()
    query = (
        InjuryRecord.query
        .join(Athlete, InjuryRecord.athlete_id == Athlete.athlete_id)
    )
    if search:
        if search.isdigit():
            query = query.filter(
                db.or_(InjuryRecord.injury_id == int(search),
                       InjuryRecord.athlete_id == int(search),
                       Athlete.full_name.ilike(f"%{search}%"),
                       InjuryRecord.injury_type.ilike(f"%{search}%"))
            )
        else:
            query = query.filter(
                db.or_(Athlete.full_name.ilike(f"%{search}%"),
                       InjuryRecord.injury_type.ilike(f"%{search}%"))
            )
    injuries = query.order_by(InjuryRecord.date_occurred.desc()).all()
    athletes = Athlete.query.order_by(Athlete.full_name).all()
    return render_template(
        "injuries/list.html", injuries=injuries, athletes=athletes, search=search
    )


@app.route("/injuries/add", methods=["GET", "POST"])
@login_required
def injury_add():
    athletes = Athlete.query.order_by(Athlete.full_name).all()

    if request.method == "POST":
        injury = InjuryRecord(
            athlete_id=request.form.get("athlete_id", type=int),
            injury_type=request.form.get("injury_type", "").strip(),
            severity=request.form.get("severity", "").strip(),
            date_occurred=request.form.get("date_occurred") or None,
            recovery_status=request.form.get("recovery_status", "").strip(),
            notes=request.form.get("notes", "").strip() or None,
        )
        db.session.add(injury)
        db.session.commit()
        flash("Injury record added successfully.", "success")
        return redirect(url_for("injuries_list"))

    return render_template("injuries/form.html", injury=None, athletes=athletes)


@app.route("/injuries/<int:id>/edit", methods=["GET", "POST"])
@login_required
def injury_edit(id):
    injury = db.session.get(InjuryRecord, id)
    if not injury:
        flash("Injury record not found.", "danger")
        return redirect(url_for("injuries_list"))

    athletes = Athlete.query.order_by(Athlete.full_name).all()

    if request.method == "POST":
        injury.athlete_id = request.form.get("athlete_id", type=int)
        injury.injury_type = request.form.get("injury_type", "").strip()
        injury.severity = request.form.get("severity", "").strip()
        injury.date_occurred = request.form.get("date_occurred") or None
        injury.recovery_status = request.form.get("recovery_status", "").strip()
        injury.notes = request.form.get("notes", "").strip() or None
        db.session.commit()
        flash("Injury record updated successfully.", "success")
        return redirect(url_for("injuries_list"))

    return render_template("injuries/form.html", injury=injury, athletes=athletes)


@app.route("/injuries/<int:id>/delete", methods=["POST"])
@login_required
def injury_delete(id):
    injury = db.session.get(InjuryRecord, id)
    if not injury:
        flash("Injury record not found.", "danger")
    else:
        db.session.delete(injury)
        db.session.commit()
        flash("Injury record deleted successfully.", "success")
    return redirect(url_for("injuries_list"))


# ═══════════════════════════════════════════════════════════════════════════════
#  PERFORMANCE STATS
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/performance")
@login_required
def performance_list():
    search = request.args.get("search", "").strip()
    query = (
        PerformanceStat.query
        .join(Athlete, PerformanceStat.athlete_id == Athlete.athlete_id)
        .join(Sport, PerformanceStat.sport_id == Sport.sport_id)
    )
    if search:
        if search.isdigit():
            query = query.filter(
                db.or_(PerformanceStat.stat_id == int(search),
                       PerformanceStat.athlete_id == int(search),
                       Athlete.full_name.ilike(f"%{search}%"),
                       Sport.name.ilike(f"%{search}%"),
                       PerformanceStat.metric_name.ilike(f"%{search}%"))
            )
        else:
            query = query.filter(
                db.or_(Athlete.full_name.ilike(f"%{search}%"),
                       Sport.name.ilike(f"%{search}%"),
                       PerformanceStat.metric_name.ilike(f"%{search}%"))
            )
    stats = query.order_by(PerformanceStat.recorded_on.desc()).all()
    athletes = Athlete.query.order_by(Athlete.full_name).all()
    sports = Sport.query.order_by(Sport.name).all()
    return render_template(
        "performance/list.html", stats=stats, athletes=athletes, sports=sports, search=search
    )


@app.route("/performance/add", methods=["GET", "POST"])
@login_required
def performance_add():
    athletes = Athlete.query.order_by(Athlete.full_name).all()
    sports = Sport.query.order_by(Sport.name).all()

    if request.method == "POST":
        stat = PerformanceStat(
            athlete_id=request.form.get("athlete_id", type=int),
            sport_id=request.form.get("sport_id", type=int),
            metric_name=request.form.get("metric_name", "").strip(),
            value=request.form.get("value", type=float),
            recorded_on=request.form.get("recorded_on") or None,
        )
        db.session.add(stat)
        db.session.commit()
        flash("Performance stat added successfully.", "success")
        return redirect(url_for("performance_list"))

    return render_template(
        "performance/form.html", stat=None, athletes=athletes, sports=sports
    )


@app.route("/performance/<int:id>/edit", methods=["GET", "POST"])
@login_required
def performance_edit(id):
    stat = db.session.get(PerformanceStat, id)
    if not stat:
        flash("Performance stat not found.", "danger")
        return redirect(url_for("performance_list"))

    athletes = Athlete.query.order_by(Athlete.full_name).all()
    sports = Sport.query.order_by(Sport.name).all()

    if request.method == "POST":
        stat.athlete_id = request.form.get("athlete_id", type=int)
        stat.sport_id = request.form.get("sport_id", type=int)
        stat.metric_name = request.form.get("metric_name", "").strip()
        stat.value = request.form.get("value", type=float)
        stat.recorded_on = request.form.get("recorded_on") or None
        db.session.commit()
        flash("Performance stat updated successfully.", "success")
        return redirect(url_for("performance_list"))

    return render_template(
        "performance/form.html", stat=stat, athletes=athletes, sports=sports
    )


@app.route("/performance/<int:id>/delete", methods=["POST"])
@login_required
def performance_delete(id):
    stat = db.session.get(PerformanceStat, id)
    if not stat:
        flash("Performance stat not found.", "danger")
    else:
        db.session.delete(stat)
        db.session.commit()
        flash("Performance stat deleted successfully.", "success")
    return redirect(url_for("performance_list"))


@app.route("/performance/chart")
@login_required
def performance_chart():
    athlete_id = request.args.get("athlete_id", type=int)
    sport_id = request.args.get("sport_id", type=int)
    metric = request.args.get("metric", "").strip()

    if not (athlete_id and sport_id and metric):
        flash("Missing parameters for chart.", "danger")
        return redirect(url_for("performance_list"))

    athlete = db.session.get(Athlete, athlete_id)
    sport = db.session.get(Sport, sport_id)
    if not athlete or not sport:
        flash("Athlete or sport not found.", "danger")
        return redirect(url_for("performance_list"))

    # Get performance data for this athlete+sport+metric, ordered by date
    stats = (
        PerformanceStat.query
        .filter_by(athlete_id=athlete_id, sport_id=sport_id, metric_name=metric)
        .order_by(PerformanceStat.recorded_on.asc())
        .all()
    )

    # Get all injuries for this athlete
    injuries = (
        InjuryRecord.query
        .filter_by(athlete_id=athlete_id)
        .order_by(InjuryRecord.date_occurred.asc())
        .all()
    )

    # Build chart data
    chart_dates = json.dumps([s.recorded_on.strftime("%Y-%m-%d") for s in stats if s.recorded_on])
    chart_values = json.dumps([float(s.value) for s in stats if s.recorded_on])

    # Build injury annotations
    injury_data = json.dumps([
        {
            "date": inj.date_occurred.strftime("%Y-%m-%d") if inj.date_occurred else None,
            "type": inj.injury_type or "Unknown",
            "severity": inj.severity or "unknown",
        }
        for inj in injuries if inj.date_occurred
    ])

    return render_template(
        "performance/chart.html",
        athlete=athlete,
        sport=sport,
        metric=metric,
        stats=stats,
        chart_dates=chart_dates,
        chart_values=chart_values,
        injury_data=injury_data,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  RUN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app.run(debug=True)
