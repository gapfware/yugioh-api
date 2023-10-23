from sqlalchemy import func
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app.config.db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    decks = relationship('Deck', backref='user')
    updated_at = Column(TIMESTAMP, nullable=False,
                        server_default=func.now(), onupdate=func.now())
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    @classmethod
    def create_user(cls, db, user_data):
        user = cls(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    def get_users(cls, db):
        return db.query(cls).all()

    @classmethod
    def get_user_by_id(cls, db, user_id):
        return db.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def get_user_by_username(cls, db, username):
        return db.query(cls).filter(cls.username == username).first()

    @classmethod
    def update_user(cls, db, user_id, user_data):
        user = cls.get_user_by_id(db, user_id)
        user.username = user_data['username']
        user.password = user_data['password']
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    def delete_user(cls, db, user_id):
        user = cls.get_user_by_id(db, user_id)
        db.delete(user)
        db.commit()
        return user
