from fastapi import FastAPI
from app.routers.card import cards
from app.routers.deck import decks



app = FastAPI()
app.include_router(cards, prefix='/cards', tags=['cards'])
app.include_router(decks, prefix='/decks', tags=['decks'])