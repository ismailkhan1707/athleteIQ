"""Test user management and chart route."""
import urllib.request
import urllib.parse
import http.cookiejar
import sys
import os
sys.path.insert(0, os.getcwd())

from app import app, db
from models import User, PerformanceStat

base = "http://127.0.0.1:5000"

with app.app_context():
    user = User.query.first()
    stat = PerformanceStat.query.first()

# Login
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cj),
    urllib.request.HTTPRedirectHandler()
)
data = urllib.parse.urlencode({"username": user.username, "password": "x"}).encode()
req = urllib.request.Request(base + "/login", data=data, method="POST")
opener.open(req)
print(f"Logged in as {user.username}\n")

# Test user management routes
tests = [
    ("/users", "Users list"),
    ("/users/add", "Add user form"),
]
print("=== User Management ===")
for route, desc in tests:
    try:
        req = urllib.request.Request(base + route)
        resp = opener.open(req)
        body = resp.read().decode("utf-8", errors="replace")
        has_sidebar = "sidebar-nav" in body
        print(f"  [{'OK' if resp.status == 200 and has_sidebar else 'FAIL'}] {desc:25s} {route:20s} -> {resp.status}")
    except Exception as e:
        print(f"  [ERR] {desc:25s} -> {e}")

# Test adding a user
print("\n=== Add User ===")
data = urllib.parse.urlencode({"username": "testuser123"}).encode()
try:
    req = urllib.request.Request(base + "/users/add", data=data, method="POST")
    resp = opener.open(req)
    body = resp.read().decode("utf-8", errors="replace")
    has_testuser = "testuser123" in body
    print(f"  Created 'testuser123': {has_testuser}")
except Exception as e:
    print(f"  Error: {e}")

# Test chart
print("\n=== Performance Chart ===")
if stat:
    params = urllib.parse.urlencode({
        "athlete_id": stat.athlete_id,
        "sport_id": stat.sport_id,
        "metric": stat.metric_name
    })
    url = f"{base}/performance/chart?{params}"
    try:
        req = urllib.request.Request(url)
        resp = opener.open(req)
        body = resp.read().decode("utf-8", errors="replace")
        has_chart = "performanceTrendChart" in body
        has_injury_data = "data-injuries" in body
        # No annotation plugin reference
        no_annotation = "annotation" not in body.lower() or "injuryAtPoint" in body
        print(f"  Chart page: {resp.status} (canvas: {has_chart}, injury data: {has_injury_data})")
    except Exception as e:
        print(f"  Error: {e}")

# Check sidebar has Users link
print("\n=== Sidebar ===")
try:
    req = urllib.request.Request(base + "/")
    resp = opener.open(req)
    body = resp.read().decode("utf-8", errors="replace")
    has_users_link = "users_list" in body or "Users" in body
    print(f"  Sidebar has Users link: {has_users_link}")
except Exception as e:
    print(f"  Error: {e}")

# Cleanup: delete test user
with app.app_context():
    tu = User.query.filter_by(username="testuser123").first()
    if tu:
        db.session.delete(tu)
        db.session.commit()
        print("\n  Cleaned up test user")

print("\nAll tests done!")
