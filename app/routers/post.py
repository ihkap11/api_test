from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: UUID = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Posts)
        .filter(models.Posts.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


@router.get("/{id}", response_model=schemas.PostResponse)
async def get_post_by_id(id: UUID, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found."
        )

    return post


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(oauth2.get_current_user),
):
    new_post = models.Posts(owner_id=current_user, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.patch("/{id}", response_model=schemas.PostResponse)
async def update_post(
    id: UUID,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(oauth2.get_current_user),
):
    updated_post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = updated_post_query.first()
    if post and post.owner_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorised request."
        )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found."
        )

    updated_post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post


@router.delete("/{id}")
async def delete_post_by_id(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(oauth2.get_current_user),
):
    deleted_post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = deleted_post_query.first()
    if post and post.owner_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorised request."
        )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found."
        )
    deleted_post_query.delete(synchronize_session=False)

    db.commit()

    return {"status": "Item deleted successfully"}
