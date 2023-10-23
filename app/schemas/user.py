from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    id: Optional[int] = None
    username: str
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


class UserCreate(UserBase):
    username: str
    password: str