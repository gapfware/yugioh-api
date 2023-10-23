from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.card import CardBase
from app.config.dependencies import get_db
from app.models.card import Card

cards = APIRouter()

@cards.get('/', response_model=list[CardBase], status_code=200)
def get_cards(db: Session = Depends(get_db)):
    return db.query(Card).all()