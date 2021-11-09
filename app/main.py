from fastapi import FastAPI, Depends
from fastapi import Response
from sqlalchemy.orm.session import Session
from starlette import status
from schemas import Post
from fastapi import HTTPException
from .database import engine_, get_db, Session
from . import models

models.Base.metadata.create_all(bind=engine_)

app = FastAPI()

GET_POSTS = """SELECT * FROM posts"""
CREATE_POST = """INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *"""
GET_POST_BY_ID = """SELECT * FROM posts WHERE id=%s"""
DELETE_POST_BY_ID = """DELETE FROM posts WHERE id=%s RETURNING *"""
UPDATE_POST_BY_ID = """UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING *"""

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]


@app.get("/")
async def root():
    return {"message": "hello world"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"status": "success", "posts": posts}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    return {"posts": db.query(models.Post).all()}


@app.post("/posts")
async def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "created post", "data": new_post}


@app.post("/posts/{id}")
async def get_post_id(
    id: int, db: Session = Depends(get_db)
):  # should be an int for the sake of validation
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return {"data": post}


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
async def update_post_id(id: int, post: Post, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == id)
    if not db_post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    db_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"detail": "update successful"}
