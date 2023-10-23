from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from app.config.dependencies import get_db
from app.models.deck import Deck

decks = APIRouter()

@decks.get('/decks/', tags=['decks'])
def get_decks(db: Session = Depends(get_db)):
    decks = db.query(Deck).options(joinedload(Deck.cards)).all()
    return decks