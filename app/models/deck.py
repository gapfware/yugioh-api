from sqlalchemy import func
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.deck_card import DeckCard
from sqlalchemy.orm import joinedload
from app.config.db import Base


class Deck(Base):
    __tablename__ = 'decks'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    card_deck = relationship(
        'Card', viewonly=True, secondary='deck_cards', backref=backref('cards', lazy='dynamic'))
    updated_at = Column(TIMESTAMP, nullable=False,
                        server_default=func.now(), onupdate=func.now())
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    cards = relationship('Card', secondary='deck_cards',
                         back_populates='decks')
    owner = relationship('User', back_populates='decks')

    deck_cards = relationship(
        'DeckCard', back_populates='deck')

    @classmethod
    def create_deck(cls, db, deck_data):
        deck = cls(**deck_data)
        db.add(deck)
        db.commit()
        db.refresh(deck)
        return deck

    @classmethod
    def get_decks(cls, db):
        return db.query(cls).options(joinedload(cls.cards)).all()

    @classmethod
    def get_deck_by_id(cls, db, deck_id):
        return db.query(cls).options(joinedload(cls.cards)).filter(cls.id == deck_id).first()

    @classmethod
    def get_deck_by_name(cls, db, deck_name):
        return db.query(cls).filter(cls.name == deck_name).first()

    @classmethod
    def get_decks_by_owner_id(cls, db, owner_id):
        return db.query(cls).filter(cls.owner_id == owner_id).all()

    @classmethod
    def update_deck(cls, db, deck_id, deck_data):
        deck = cls.get_deck_by_id(db, deck_id)
        deck.name = deck_data['name']
        deck.owner_id = deck_data['owner_id']
        db.commit()
        db.refresh(deck)
        return deck

    @classmethod
    def delete_deck(cls, db, deck_id):
        deck = cls.get_deck_by_id(db, deck_id)
        db.delete(deck)
        db.commit()
        return deck

    @classmethod
    def add_card_to_deck(cls, db, deck_id, card_id):
        deck_card = DeckCard(deck_id=deck_id, card_id=card_id)

        db.add(deck_card)
        db.commit()
        return {'message': 'Card added to deck'}

    @classmethod
    def remove_card_from_deck(cls, db, deck_id, card_id):
        db.query(DeckCard).filter(DeckCard.deck_id == deck_id,
                                  DeckCard.card_id == card_id).delete()
        db.commit()
        return {'message': 'Card removed from deck'}


Deck.card_deck = relationship(
    'DeckCard', back_populates='deck', overlaps='deck_cards')
Deck.deck_cards = relationship(
    'DeckCard', back_populates='deck', overlaps='card_deck')
