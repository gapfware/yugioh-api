from sqlalchemy import func
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import relationship,backref
from sqlalchemy import Column, Integer, String, ForeignKey

from app.config.db import Base


class Deck(Base):
    __tablename__ = 'decks'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    card_deck = relationship(
        'Card', secondary='deck_cards', backref=backref('cards', lazy='dynamic'))
    updated_at = Column(TIMESTAMP, nullable=False,
                        server_default=func.now(), onupdate=func.now())
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    cards = relationship('Card', secondary='deck_cards',
                         back_populates='decks')
    deck_cards = relationship(
        'DeckCard', back_populates='deck', overlaps='card_deck')
    decks = relationship('DeckCard', back_populates='deck',
                         overlaps='card_deck')

Deck.card_deck = relationship(
    'DeckCard', back_populates='deck', overlaps='deck_cards')
Deck.deck_cards = relationship(
    'DeckCard', back_populates='deck', overlaps='card_deck')
