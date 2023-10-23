from fastapi import FastAPI
from app.models.base import Base
from app.config.db import engine

app = FastAPI()
