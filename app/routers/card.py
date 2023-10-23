from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.card import CardBase
from app.config.dependencies import get_db
from app.controllers.card import CardController

cards = APIRouter()
controller = CardController


@cards.get('/', response_model=list[CardBase], status_code=200)
def get_cards(db: Session = Depends(get_db)):
    return controller(db).get_cards()


@cards.get('/{card_id}', response_model=CardBase, status_code=200)
def get_card(card_id: int, db: Session = Depends(get_db)):
    return controller(db).get_card(card_id)


@cards.post('/', response_model=CardBase, status_code=201)
def create_card(card: CardBase, db: Session = Depends(get_db)):
    return controller(db).create_card(card)


@cards.put('/{card_id}', response_model=CardBase, status_code=200)
def update_card(card_id: int, card: CardBase, db: Session = Depends(get_db)):
    return controller(db).update_card(card_id, card)


@cards.delete('/{card_id}', status_code=200)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    return controller(db).delete_card(card_id)
