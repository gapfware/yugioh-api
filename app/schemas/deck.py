from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .card import CardInDeck


class DeckBase(BaseModel):
    id: Optional[int] = None
    name: str
    owner_id: int
    cards: list[CardInDeck] = []
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


class DeckCreate(BaseModel):
    name: str
    owner_id: int



