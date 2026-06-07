from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event
from app.schemas import EventCreate, EventResponse

from typing import List
from app.models import Registration
from app.schemas import EventView

from datetime import datetime

from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.post("/events", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):

    existing_event = db.query(Event).filter(Event.name == event.name).first()

    if existing_event:
        raise HTTPException(
            status_code=400,
            detail="Event name already exists"
        )

    new_event = Event(
        name=event.name,
        total_seats=event.total_seats,
        event_date=event.event_date
    )

    try:
        db.add(new_event)
        db.commit()
        db.refresh(new_event)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Event name already exists"
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while creating event"
        )

    return new_event

@router.get("/events", response_model=List[EventView])
def get_events(
    upcoming: bool = False,
    sort_by: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(Event)

    if upcoming:
        query = query.filter(Event.event_date > datetime.now())

    if sort_by == "date":
        query = query.order_by(Event.event_date)

    events = query.all()

    result = []

    for event in events:
        active_registrations = db.query(Registration).filter(
            Registration.event_id == event.id,
            Registration.status == "ACTIVE"
        ).count()

        result.append(
            {
                "id": event.id,
                "name": event.name,
                "total_seats": event.total_seats,
                "available_seats": event.total_seats - active_registrations,
                "total_registrations": active_registrations
            }
        )

    return result