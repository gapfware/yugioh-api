from sqlalchemy import func
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, CheckConstraint
from app.schemas.card import CardBase
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

    @classmethod
    def create_card(cls, db, card_data):
        card = cls(**card_data)
        db.add(card)
        db.commit()
        db.refresh(card)
        return card

    @classmethod
    def get_cards(cls, db)-> CardBase: 
        return db.query(cls).all()

    @classmethod
    def get_card_by_id(cls, db, card_id):
        return db.query(cls).filter(cls.id == card_id).first()

    @classmethod
    def get_card_by_name(cls, db, card_name):
        return db.query(cls).filter(cls.name == card_name).first()

    @classmethod
    def update_card(cls, db, card_id, card_data):
        card = cls.get_card_by_id(db, card_id)
        for key, value in card_data.items():
            setattr(card, key, value)
        db.commit()
        db.refresh(card)
        return card

    @classmethod
    def delete_card(cls, db, card_id):
        card = cls.get_card_by_id(db, card_id)
        db.delete(card)
        db.commit()
        return card
