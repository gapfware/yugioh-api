from sqlalchemy.orm import Session
from app.config.db import SessionLocal


def get_db() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
