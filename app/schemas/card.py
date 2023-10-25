from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CardBase(BaseModel):
    id: Optional[int] = None
    name: str
    type: str | None = None
    attack: Optional[int] = None
    defense: Optional[int] = None
    description: str
    image_url: Optional[str] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    def dict_exclude_protected(self):
        return self.model_dump(exclude={'id', 'updated_at', 'created_at'})


class CardInDeck(CardBase):
    quantity: int = 0


class CardCreate(BaseModel):
    name: str
    type: str | None = None
    attack: Optional[int] = None
    defense: Optional[int] = None
    description: str
    image_url: Optional[str] = None


class CardUpdate(BaseModel):
    name: str
    attack: Optional[int] = None
    defense: Optional[int] = None
    description: str
    image_url: Optional[str] = None
