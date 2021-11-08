import enum
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from schemas import Post

app = FastAPI()

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]


def find_post(id: int):
    for idx, post in enumerate(my_posts):
        if post.get("id") == id:
            return idx, post
    return None, None


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    id = my_posts[-1].get("id") + 1
    new_post = post.dict()
    new_post.update({"id": id})
    my_posts.append(new_post)
    return {"message": "created post", "body": new_post}


@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    idx, post = find_post(id)
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no post found for id: {id}"
        )
    return {"detail": f"here is the post with id: {id}", "post": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    idx, post = find_post(id)

    my_posts.remove(post)
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no post found for id: {id}"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    idx, post_dict = find_post(id)
    post_dict["title"] = post.title
    post_dict["content"] = post.content
    my_posts[idx] = post_dict
    return {"detail": "updated post"}
