from fastapi import FastAPI
from app.routers.card import cards
from app.routers.deck import decks
from app.routers.user import users

app = FastAPI()


app.include_router(cards, prefix='/cards', tags=['cards'])
app.include_router(decks, prefix='/decks', tags=['decks'])
app.include_router(users, prefix='/users', tags=['users'])

