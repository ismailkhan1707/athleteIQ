"""Create a single admin user for AthleteIQ."""
import sys, hashlib
sys.path.insert(0, ".")
from app import app, db
from models import User

with app.app_context():
    count = User.query.count()
    print(f"Current users: {count}")
    
    if count == 0:
        pw_hash = hashlib.sha256("admin_athleteiq".encode()).hexdigest()
        user = User(username="admin", password_hash=pw_hash)
        db.session.add(user)
        db.session.commit()
        print("Created user: admin")
    else:
        print("Users already exist, skipping.")
    
    print(f"Total users: {User.query.count()}")
