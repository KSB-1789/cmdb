import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User

def promote_to_admin(email):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_admin = True
            db.session.commit()
            print(f"User {user.username} has been promoted to admin.")
        else:
            print("User not found.")

if __name__ == "__main__":
    email = input("Enter the email of the user to promote to admin: ")
    promote_to_admin(email)

user = User.query.filter_by(email='user@example.com').first()
if user:
    user.is_admin = True
    db.session.commit()
    print(f"User {user.username} has been promoted to admin.")
else:
    print("User not found.") 