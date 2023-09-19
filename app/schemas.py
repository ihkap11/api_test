from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserCreateResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration: float
    attended: Optional[bool] = True


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: UUID
    created_at: datetime
    owner_id: UUID
    owner: UserCreateResponse

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
