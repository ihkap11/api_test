from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserCreateResponse,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hashify(user.password)
    existing_user = (
        db.query(models.Users).filter(models.Users.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists."
        )
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get(
    "/{id}",
    response_model=schemas.UserCreateResponse,
)
def get_user_by_id(id: UUID, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, details=f"User {id} not found."
        )
    return user


@router.get(
    "/",
    response_model=List[schemas.UserCreateResponse],
)
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()

    return users
