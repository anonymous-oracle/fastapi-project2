from fastapi import FastAPI
from fastapi.params import Body
from schemas import Post

app = FastAPI()

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/posts")
async def get_posts():
    return {"data": ["List", "of", "posts"]}


# # extracting post request body/payload data
# @app.post("/createposts")
# # the '...' dots indicate as many as needed
# async def create_post(payload: dict = Body(...)):
#     return {"message": "created post", "body": payload}


@app.post("/posts")
async def create_post(post: Post):
    print(post.dict())
    return {"message": "created post", "body": post}
