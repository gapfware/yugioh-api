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


