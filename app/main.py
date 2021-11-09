from fastapi import FastAPI, Depends
from fastapi import Response
from sqlalchemy.orm.session import Session
from starlette import status
from fastapi import HTTPException

from app.hashing import gen_salt, hash_pwd
from .database import engine_, get_db, Session
from . import models, schemas

models.Base.metadata.create_all(bind=engine_)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    return {"posts": db.query(models.Post).all()}


@app.post("/posts", response_model=schemas.PostResponse)
async def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.post("/posts/{id}", response_model=schemas.PostResponse)
async def get_post_id(
    id: int, db: Session = Depends(get_db)
):  # should be an int for the sake of validation
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_id(
    id: int, db: Session = Depends(get_db)
):  # should be an int for the sake of validation
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    # use this for efficient db operation
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post_id(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == id)
    if not db_post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    db_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"detail": "update successful"}


@app.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    salt = gen_salt()
    user.password = hash_pwd(user.password, salt)
    new_user = models.User(**user.dict(), salt=salt)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
