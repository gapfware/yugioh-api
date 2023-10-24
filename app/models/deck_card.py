from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey
from app.config.db import Base


class DeckCard(Base):
    __tablename__ = 'deck_cards'
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey('cards.id'))
    deck_id = Column(Integer, ForeignKey('decks.id'))

    deck = relationship('Deck', back_populates='deck_cards', )
    card = relationship('Card', back_populates='deck_cards')

    @classmethod
    def remove_cards(cls, db, deck_id):
        db.query(cls).filter(cls.deck_id == deck_id).delete()
        db.commit()
        return True
