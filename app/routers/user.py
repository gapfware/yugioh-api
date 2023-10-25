
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserBase, UserCreate
from app.config.dependencies import get_db
from app.controllers.user import UserController
from app.schemas.user import UserBase



users = APIRouter()
controller = UserController


@users.get('/', response_model=list[UserBase], status_code=200)
def get_users(db: Session = Depends(get_db)):
    return controller(db).get_users()


@users.get('/{user_id}', response_model=UserBase, status_code=200, )
def get_user(user_id: int, db: Session = Depends(get_db)):
    return controller(db).get_user(user_id)


@users.post('/', response_model=UserBase, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return controller(db).create_user(user)


@users.put('/{user_id}', response_model=UserBase, status_code=200)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return controller(db).update_user(user_id, user)


@users.delete('/{user_id}', status_code=200)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return controller(db).delete_user(user_id)
