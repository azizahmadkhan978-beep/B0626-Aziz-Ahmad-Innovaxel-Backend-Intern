from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event, Registration
from app.schemas import RegistrationCreate, RegistrationResponse

from sqlalchemy.exc import IntegrityError

from app.config import DEFAULT_REGISTRATION_STATUS, CANCELLED_REGISTRATION_STATUS

router = APIRouter()


@router.post("/register", response_model=RegistrationResponse)
def register_user(registration: RegistrationCreate, db: Session = Depends(get_db)):

    event = db.query(Event).filter(Event.id == registration.event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    existing_registration = db.query(Registration).filter(
        Registration.event_id == registration.event_id,
        Registration.user_name == registration.user_name,
        Registration.status == DEFAULT_REGISTRATION_STATUS
    ).first()

    if existing_registration:
        raise HTTPException(status_code=400, detail="User already registered for this event")

    active_registrations = db.query(Registration).filter(
        Registration.event_id == registration.event_id,
        Registration.status == DEFAULT_REGISTRATION_STATUS
    ).count()

    remaining_seats = event.total_seats - active_registrations
    if remaining_seats <= 0:
        raise HTTPException(
            status_code=400,
            detail="Event is full"
        )
    new_registration = Registration(
        user_name=registration.user_name,
        event_id=registration.event_id,
        status=DEFAULT_REGISTRATION_STATUS
    )

    try:
        db.add(new_registration)
        db.commit()
        db.refresh(new_registration)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Duplicate registration is not allowed"
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while registering user"
        )
    return new_registration
@router.delete("/register/{registration_id}")
def cancel_registration(
    registration_id: int,
    db: Session = Depends(get_db)
):

    registration = db.query(Registration).filter(
        Registration.id == registration_id
    ).first()

    if not registration:
        raise HTTPException(
            status_code=404,
            detail="Registration not found"
        )

    if registration.status == CANCELLED_REGISTRATION_STATUS:
        raise HTTPException(
            status_code=400,
            detail="Registration already cancelled"
        )

    registration.status = CANCELLED_REGISTRATION_STATUS

    db.commit()

    return {
        "message": "Registration cancelled successfully"
    }
