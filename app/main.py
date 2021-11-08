from fastapi import FastAPI
from schemas import Post
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

GET_POSTS = """SELECT * FROM posts"""

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="1234",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/posts")
async def get_posts():
    cursor.execute(GET_POSTS)
    posts = cursor.fetchall()
    print(posts)
    return {"posts": posts}


# # extracting post request body/payload data
# @app.post("/createposts")
# # the '...' dots indicate as many as needed
# async def create_post(payload: dict = Body(...)):
#     return {"message": "created post", "body": payload}


@app.post("/posts")
async def create_post(post: Post):
    print(post.dict())
    return {"message": "created post", "body": post}
