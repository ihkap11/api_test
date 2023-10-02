from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(oauth2.get_current_user),
):
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user
    )
    found_vote = vote_query.first()
    if vote.vote_dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user} has already voted on the post {vote.post_id}",
            )
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Successfully added vote."}

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exist."
            )

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote."}


@router.get("/votes", status_code=status.HTTP_201_CREATED)
def read_vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(oauth2.get_current_user),
):
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user
    )
    found_vote = vote_query.first()
    if vote.vote_dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user} has already voted on the post {vote.post_id}",
            )
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Successfully added vote."}

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exist."
            )

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote."}
