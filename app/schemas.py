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