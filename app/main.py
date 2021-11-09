from fastapi import FastAPI, Depends
from fastapi.openapi.models import Response
from sqlalchemy.orm.session import Session
from starlette import status
from schemas import Post
from .database import engine_, get_db, Session
from .models import Base

Base.metadata.create_all(bind=engine_)

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

@app.get('/sqlalchemy')
def test_posts(db:Session = Depends(get_db)):
    
    return {'status':'success'}

@app.get("/posts")
async def get_posts():
    cursor.execute(GET_POSTS)
    posts = cursor.fetchall()
    print(posts)
    return {"posts": posts}


@app.post("/posts")
async def create_post(post: Post):
    cursor.execute(
        CREATE_POST, (post.title, post.content)
    )  # this is a good method to follow because this formatting is not vulnerable to sql injection attacks
    new_post = cursor.fetchone()
    # commit the changes
    conn.commit()
    return {"message": "created post", "body": new_post}


@app.post("/posts/{id}")
async def get_post_id(id: int):  # should be an int for the sake of validation
    cursor.execute(GET_POST_BY_ID, (str(id)))
    post = cursor.fetchone()
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_id(id: int, response: Response):  # should be an int for the sake of validation
    cursor.execute(DELETE_POST_BY_ID, (str(id)))
    post = cursor.fetchone()
    conn.commit()
    return response

@app.put("/posts/{id}")
async def update_post_id(id: int, post: Post):
    cursor.execute(UPDATE_POST_BY_ID, (post.title, post.content, str(id)))
    post = cursor.fetchone()
    conn.commit()
    return {"updated": post}
