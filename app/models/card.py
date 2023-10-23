from sqlalchemy import func
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, CheckConstraint
from app.config.db import Base


class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True, unique=True)
    type = Column(String(50), nullable=False)
    attack = Column(Integer)
    defense = Column(Integer)
    description = Column(Text())
    image_url = Column(String(255))
    updated_at = Column(TIMESTAMP, nullable=False,
                        server_default=func.now(), onupdate=func.now())
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    decks = relationship('Deck', secondary='deck_cards',
                         back_populates='cards')
    deck_cards = relationship('DeckCard', back_populates='card')

    __table_args__ = (
        CheckConstraint(
            type.in_(['monster', 'spell', 'trap']), name='type_check'),
    )
