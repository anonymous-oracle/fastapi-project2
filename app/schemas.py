from datetime import datetime
from os import access
from typing import Optional
from pydantic import BaseModel


class BasePost(BaseModel):
    class Config:
        orm_mode = True


class Post(BasePost):
    title: str
    content: str
    published: bool = True


class PostResponse(BasePost):
    title: str
    content: str


class BaseUser(BaseModel):
    class Config:
        orm_mode = True


class User(BaseUser):
    email: str
    password: str


class UserResponse(BaseUser):
    id: int
    email: str
    created_at: datetime


class UserLogin(BaseUser):
    email: str
    password: str

# access token schemas
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None