from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.deck import DeckCreate, DeckBase
from app.config.dependencies import get_db
from app.controllers.deck import DeckController

decks = APIRouter()
controller = DeckController


@decks.get('/', response_model=list[DeckBase], status_code=200)
def get_decks(db: Session = Depends(get_db)):
    return controller(db).get_decks()


@decks.get('/{deck_id}', response_model=DeckBase, status_code=200)
def get_deck(deck_id: int, db: Session = Depends(get_db)):
    return controller(db).get_deck(deck_id)


@decks.post('/', response_model=DeckBase, status_code=201)
def create_deck(deck: DeckCreate, db: Session = Depends(get_db)):
    return controller(db).create_deck(deck)


@decks.put('/{deck_id}', response_model=DeckBase, status_code=200)
def update_deck(deck_id: int, deck: DeckBase, db: Session = Depends(get_db)):
    return controller(db).update_deck(deck_id, deck)


@decks.delete('/{deck_id}', status_code=200)
def delete_deck(deck_id: int, db: Session = Depends(get_db)):
    return controller(db).delete_deck(deck_id)
