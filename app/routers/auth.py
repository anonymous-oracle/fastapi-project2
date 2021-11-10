from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, models
from ..database import Session, get_db
from ..hashing import check_pwd

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )
    if not user or not check_pwd(user_credentials.password, user.password, user.salt):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    # create a token

    return {"token": "example token"}
