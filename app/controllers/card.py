from sqlalchemy.orm import Session
from app.models.card import Card
from app.schemas.card import CardBase, CardCreate
from fastapi import HTTPException


class CardController:
    def __init__(self, db: Session):
        self.db = db

    def get_cards(self):
        return Card.get_cards(self.db)

    def get_card(self, card_id: int):
        card = Card.get_card_by_id(self.db, card_id)
        if not card:
            raise HTTPException(status_code=404, detail='Card not found')
        return card

    def create_card(self, card: CardCreate):
        existing_card = self.db.query(Card).filter(
            Card.name == card.name).first()
        if existing_card:
            raise HTTPException(
                status_code=400, detail=f'A card with the name "{card.name}" already exists.')
        if card.type.lower() not in ['monster', 'spell', 'trap']:
            raise HTTPException(
                status_code=400, detail='Card type must be monster, spell, or trap')
        if card.type == 'monster' and (card.attack is None or card.defense is None):
            raise HTTPException(
                status_code=400, detail='Attack and defense are required for monster cards')
        if card.type.lower() != 'monster':
            card.attack = None
            card.defense = None
        card.type = card.type.lower()
        return Card.create_card(self.db, card.dict_exclude_protected())

    def update_card(self, card_id: int, card: CardCreate):
        existing_card = Card.get_card_by_id(self.db, card_id)
        if not existing_card:
            raise HTTPException(status_code=404, detail='Card not found')
        if Card.get_card_by_name(self.db, card.name) and card.name != existing_card.name:
            raise HTTPException(
                status_code=400, detail=f'A card with the name "{card.name}" already exists.')
        if not existing_card:
            raise HTTPException(status_code=404, detail='Card not found')
        if card.type != existing_card.type.lower():
            raise HTTPException(
                status_code=400, detail='Card type cannot be changed')
        if card.type == 'monster' and (card.attack is None or card.defense is None):
            raise HTTPException(
                status_code=400, detail='Attack and defense are required for monster cards')
        return Card.update_card(self.db, card_id, card.dict_exclude_protected())

    def delete_card(self, card_id: int):
        card = Card.get_card_by_id(self.db, card_id)
        if not card:
            raise HTTPException(status_code=404, detail='Card not found')
        card = Card.delete_card(self.db, card_id)
        return {'message': 'Card deleted'}
