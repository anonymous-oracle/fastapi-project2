from typing import Optional
from ..oauth2 import get_current_user
from .. import schemas, models
from fastapi import status, APIRouter
from ..database import Session, get_db
from fastapi import Depends, HTTPException, Response

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/")
async def get_posts(
    db: Session = Depends(get_db),
    limit: int = 5,
    skip: int = 0,
    search: Optional[str] = "",
):
    # limit is a url/query parameter which returns only the limit number of posts and skip is used to skip a certain number of posts from the start
    # the search query is passed to use basic search functionality
    return {
        "posts": db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    }


@router.post("/", response_model=schemas.PostResponse)
async def create_post(
    post: schemas.Post,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user),
):
    new_post = models.Post(**post.dict(), user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.post("/{id}", response_model=schemas.PostResponse)
async def get_post_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user),
):  # should be an int for the sake of validation
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user),
):  # should be an int for the sake of validation
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    # checks to delete only the post of the current user
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    # use this for efficient db operation
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
async def update_post_id(
    id: int,
    post: schemas.Post,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_query.first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    # checks to update only the posts of the current user
    if db_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"detail": "update successful"}
