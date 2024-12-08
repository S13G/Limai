from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.routers.core.models import User
from app.routers.core.responses import UserOut
from app.routers.core.schemas import UserCreate
from app.utilities.utils import hash_password

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user.email = user.email.lower()

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with that email already exists",
        )

    hashed_password = hash_password(user.password)
    user.password = hashed_password

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
