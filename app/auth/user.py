import os
from fastapi import APIRouter, HTTPException, Depends
from app.config.db import SessionLocal
from app.utils.hashing import Hasher
from datetime import timedelta, datetime
from jose import jwt, JWTError
from dotenv import load_dotenv
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.schemas.user import UserBase, UserCreate, UserInDB
from app.config.dependencies import get_db
from app.controllers.user import UserController
from typing import Union


# TODO: Hacer que funcione para proteger las rutas
load_dotenv()
SECRET = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
oauth2_scheme = OAuth2PasswordBearer('/token')

users = APIRouter()

controller = UserController


def get_user(username: str, db: Session = Depends(get_db), ):
    user = controller(db).get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail='Could not validate credentials', headers={
                            'WWW-Authenticate': 'Bearer'})
    return UserInDB(**user.__dict__)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(username, db)

    if not user:
        raise HTTPException(status_code=401, detail='Could not validate credentials', headers={
                            'WWW-Authenticate': 'Bearer'})
    if not Hasher.verify_password(password, user.password):
        raise HTTPException(status_code=401, detail='Incorrect password', headers={
                            'WWW-Authenticate': 'Bearer'})
    return user


def create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expire is None:
        time_expire = datetime.utcnow() + timedelta(minutes=15)
    else:
        time_expire = datetime.utcnow() + time_expire
    data_copy.update({'exp': time_expire})
    token_jwt = jwt.encode(data_copy, key=SECRET, algorithm=ALGORITHM)
    return token_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, key=SECRET, algorithms=[ALGORITHM])
        username = token_decode.get('sub')
        if username == None:
            raise HTTPException(status_code=401, detail='Invalid token', headers={
                                'WWW-Authenticate': 'Bearer'})
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token', headers={
            'WWW-Authenticate': 'Bearer'})
    user = get_user(username, db=SessionLocal())
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token', headers={
            'WWW-Authenticate': 'Bearer'})
    return user


@users.get('/me')
def user_me(current_user: UserBase = Depends(get_current_user)):
    return current_user


@users.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    print(user)
    access_token_expires = timedelta(minutes=30)
    acces_token_jwt = create_token(
        {'sub': user.get('username')}, access_token_expires)
    return {'access_token': acces_token_jwt, 'token_type': 'bearer'}
