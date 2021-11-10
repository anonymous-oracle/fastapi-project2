from ..oauth2 import get_current_user
from .. import schemas, models
from fastapi import status, APIRouter
from ..database import Session, get_db
from fastapi import Depends, HTTPException, Response

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/")
async def get_posts(db: Session = Depends(get_db)):
    return {"posts": db.query(models.Post).all()}


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


@router.put("/{id}")
async def update_post_id(
    id: int,
    post: schemas.Post,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user),
):
    db_post = db.query(models.Post).filter(models.Post.id == id)
    if not db_post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    db_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"detail": "update successful"}
