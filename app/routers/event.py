from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/", response_model=List[schemas.EventResponse])
async def get_events(
    db: Session = Depends(get_db),
    current_user: UUID = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    events = (
        db.query(models.Events)
        .filter(models.Events.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return events


@router.get("/{id}", response_model=schemas.EventResponse)
async def get_event_by_id(id: UUID, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM events WHERE id = %s""", str(id))
    # event = cursor.fetchone()
    event = db.query(models.Events).filter(models.Events.id == id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Event {id} not found."
        )

    return event


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.EventResponse
)
async def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """INSERT INTO events (title, description, duration, attended) VALUES (%s,%s,%s,%s) RETURNING *""",
    #     (event.title, event.description, event.duration, event.attended),
    # )
    new_event = models.Events(owner_id=current_user, **event.model_dump())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


@router.patch("/{id}", response_model=schemas.EventResponse)
async def update_event(
    id: UUID,
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """UPDATE posts SET title = %s, description = %s, duration = %s, attended = %s RETURNING *""",
    #     event.title,
    #     event.description,
    #     event.duration,
    #     event.attended,
    # )
    # updated_event_query = cursor.fetchone()
    # conn.commit()
    updated_event_query = db.query(models.Events).filter(models.Events.id == id)
    event = updated_event_query.first()
    if event and event.owner_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorised request."
        )
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Event {id} not found."
        )

    updated_event_query.update(event.model_dump(), synchronize_session=False)
    db.commit()
    return event


@router.delete("/{id}")
async def delete_item_by_id(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM events WHERE id = %s RETURNING *""", str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_event_query = db.query(models.Events).filter(models.Events.id == id)
    event = deleted_event_query.first()
    if event and event.owner_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorised request."
        )
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Event {id} not found."
        )
    deleted_event_query.delete(synchronize_session=False)

    db.commit()

    return {"status": "Item deleted successfully"}
