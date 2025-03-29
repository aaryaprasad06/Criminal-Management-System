from sqlalchemy.orm import Session
from sqlalchemy import text
from db import SessionLocal

def test_db_connection():
    try:
        db: Session = SessionLocal()
        db.execute(text("SELECT 1"))  # Use `text()` for raw SQL
        print("✅ Database connection is working!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    finally:
        db.close()

test_db_connection()
