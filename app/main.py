from fastapi import FastAPI
from .database import engine_
from . import models
from .routers import users, posts, auth

models.Base.metadata.create_all(bind=engine_)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}
