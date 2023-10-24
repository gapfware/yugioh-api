from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeckBase(BaseModel):
    id: Optional[int] = None
    name: str
    owner_id: int
    cards: Optional[list] = []
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


class DeckCreate(BaseModel):
    name: str
    owner_id: int