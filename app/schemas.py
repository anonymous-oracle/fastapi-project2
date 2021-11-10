from datetime import datetime
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
