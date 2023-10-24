from sqlalchemy.orm import Session
from app.models.user import User
from app.models.deck import Deck
from app.schemas.user import UserBase, UserCreate
from app.controllers.deck import DeckController
from fastapi import HTTPException


class UserController:
    def __init__(self, db: Session):
        self.db = db

    def get_users(self):
        return User.get_users(self.db)

    def get_user(self, user_id: int) -> UserBase:
        user = User.get_user_by_id(self.db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        return user

    def create_user(self, user: UserCreate):
        existing_user = User.get_user_by_username(self.db, user.username)
        if existing_user:
            raise HTTPException(
                status_code=400, detail=f'A user with the username "{user.username}" already exists.')
        return User.create_user(self.db, user.model_dump())

    def update_user(self, user_id: int, user: UserBase):
        existing_user = User.get_user_by_id(self.db, user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail='User not found')
        if User.get_user_by_username(self.db, user.username) and user.username != existing_user.username:
            raise HTTPException(
                status_code=400, detail=f'A user with the username "{user.username}" already exists.')
        return User.update_user(self.db, user_id, user.model_dump())

    def delete_user(self, user_id: int):
        existing_user = User.get_user_by_id(self.db, user_id)
        user_decks = Deck.get_decks_by_owner_id(self.db, user_id)
        if user_decks:
            for deck in user_decks:
                DeckController(self.db).delete_deck(deck.id)
        if not existing_user:
            raise HTTPException(status_code=404, detail='User not found')
        User.delete_user(self.db, user_id)
        return {'message': 'User deleted'}

    def get_user_decks(self, user_id: int):
        user = User.get_user_by_id(self.db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        return user.decks
