from sqlalchemy.orm import Session
from app.models.deck import Deck
from app.models.user import User
from app.schemas.deck import DeckBase, DeckCreate
from fastapi import HTTPException


class DeckController:
    def __init__(self, db: Session):
        self.db = db

    def get_decks(self):
        return Deck.get_decks(self.db)

    def get_deck(self, deck_id: int) -> DeckBase:
        deck = Deck.get_deck_by_id(self.db, deck_id)
        if not deck:
            raise HTTPException(status_code=404, detail='Deck not found')
        return deck

    def create_deck(self, deck: DeckBase):
        existing_deck = Deck.get_deck_by_name(self.db, deck.name)
        existing_deck_owner = User.get_user_by_id(self.db, deck.owner_id)

        if not existing_deck_owner:
            raise HTTPException(status_code=404, detail='User not found')

        if existing_deck:
            raise HTTPException(
                status_code=400, detail=f'A deck with the name "{deck.name}" already exists.')
        return Deck.create_deck(self.db, deck.model_dump())

    def update_deck(self, deck_id: int, deck: DeckBase):
        existing_deck = Deck.get_deck_by_id(self.db, deck_id)
        if not existing_deck:
            raise HTTPException(status_code=404, detail='Deck not found')
        if Deck.get_deck_by_name(self.db, deck.name) and deck.name != existing_deck.name:
            raise HTTPException(
                status_code=400, detail=f'A deck with the name "{deck.name}" already exists.')
        return Deck.update_deck(self.db, deck_id, deck.model_dump())

    def delete_deck(self, deck_id: int):
        existing_deck = Deck.get_deck_by_id(self.db, deck_id)
        if not existing_deck:
            raise HTTPException(status_code=404, detail='Deck not found')
        Deck.delete_deck(self.db, deck_id)
        return {'message': 'Deck deleted'}
