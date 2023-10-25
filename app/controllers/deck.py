from sqlalchemy.orm import Session
from app.models.deck import Deck
from app.models.user import User
from app.models.card import Card
from app.models.deck_card import DeckCard
from app.schemas.deck import DeckBase, DeckCreate
from fastapi import HTTPException


class DeckController:
    def __init__(self, db: Session):
        self.db = db

    def get_decks(self) -> DeckBase:
        return Deck.get_decks(self.db)

    def get_deck(self, deck_id: int) -> DeckBase:
        deck = Deck.get_deck_by_id(self.db, deck_id)
        if not deck:
            raise HTTPException(status_code=404, detail='Deck not found')
        return deck

    def create_deck(self, deck: DeckCreate) -> DeckBase:
        existing_deck = Deck.get_deck_by_name(self.db, deck.name)
        existing_deck_owner = User.get_user_by_id(self.db, deck.owner_id)

        if not existing_deck_owner:
            raise HTTPException(status_code=404, detail='User not found')

        if existing_deck:
            raise HTTPException(
                status_code=400, detail=f'A deck with the name "{deck.name}" already exists.')
        return Deck.create_deck(self.db, deck.model_dump())

    def update_deck(self, deck_id: int, deck: DeckCreate) -> DeckBase:
        print(deck_id, deck)
        existing_deck = Deck.get_deck_by_id(self.db, deck_id)
        if existing_deck.owner_id != deck.owner_id:
            raise HTTPException(
                status_code=400, detail='You cannot update the owner of the deck.')
        if not existing_deck:
            raise HTTPException(status_code=404, detail='Deck not found')
        if Deck.get_deck_by_name(self.db, deck.name) and deck.name != existing_deck.name:
            raise HTTPException(
                status_code=400, detail=f'A deck with the name "{deck.name}" already exists.')

        return Deck.update_deck(self.db, deck_id, deck.model_dump())

    def delete_deck(self, deck_id: int) -> dict:
        existing_deck = Deck.get_deck_by_id(self.db, deck_id)
        if not existing_deck:
            raise HTTPException(status_code=404, detail='Deck not found')
        DeckCard.remove_cards(self.db, existing_deck.id)
        Deck.delete_deck(self.db, deck_id)
        return {'message': 'Deck deleted'}

    def get_card_quantity(self, deck_id: int):
        deck = Deck.get_deck_by_id(self.db, deck_id)
        if not deck:
            raise HTTPException(status_code=404, detail='Deck not found')
        return len(deck.cards)

    def add_card_to_deck(self, deck_id: int, card_id: int):
        deck = Deck.get_deck_by_id(self.db, deck_id)
        card = Card.get_card_by_id(self.db, card_id)
        card_quantity = self.get_card_quantity(deck_id)
        if card_quantity >= 60:
            raise HTTPException(status_code=400, detail='Deck is full')
        if not deck:
            raise HTTPException(status_code=404, detail='Deck not found')
        if not card:
            raise HTTPException(status_code=404, detail='Card not found')
        return Deck.add_card_to_deck(self.db, deck_id, card_id)

    def remove_card_from_deck(self, deck_id: int, card_id: int):
        deck = Deck.get_deck_by_id(self.db, deck_id)
        card = Card.get_card_by_id(self.db, card_id)
        if not deck:
            raise HTTPException(status_code=404, detail='Deck not found')
        if not card:
            raise HTTPException(status_code=404, detail='Card not found')
        return Deck.remove_card_from_deck(self.db, deck_id, card_id)
