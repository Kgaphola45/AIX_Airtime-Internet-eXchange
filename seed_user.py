import sys
import os

# Ensure app module can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.models.user import User
from app.models.wallet import Wallet
from app.core.security import get_password_hash
from app.database.db import engine, Base

def seed_user():
    # Recreate tables since we deleted the DB
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    email = "man@gmail.com"
    password = "12345"
    full_name = "Emmanuel"

    try:
        # Check if exists
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"User {email} already exists with ID: {existing.id}")
            return

        # This will now be plain text based on our change
        hashed = get_password_hash(password)
        
        user = User(email=email, hashed_password=hashed, full_name=full_name)
        db.add(user)
        db.commit()
        db.refresh(user)
        
        wallet = Wallet(user_id=user.id, balance=0.0)
        db.add(wallet)
        db.commit()
        print(f"User {email} created successfully with ID: {user.id}")
        
    except Exception as e:
        print(f"Error seeding user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_user()
