from pydantic import BaseModel, field_validator
from datetime import datetime


class EventCreate(BaseModel):
    name: str
    total_seats: int
    event_date: datetime

    @field_validator("name")
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Event name cannot be empty")
        return value

    @field_validator("total_seats")
    def validate_total_seats(cls, value):
        if value <= 0:
            raise ValueError("Total seats must be greater than 0")
        return value

    @field_validator("event_date")
    def validate_event_date(cls, value):
        if value <= datetime.now():
            raise ValueError("Event date must be in the future")
        return value


class EventResponse(BaseModel):
    id: int
    name: str
    total_seats: int
    event_date: datetime

    class Config:
        from_attributes = True
class RegistrationCreate(BaseModel):
    user_name: str
    event_id: int

    @field_validator("user_name")
    def validate_user_name(cls, value):
        if not value.strip():
            raise ValueError("User name cannot be empty")
        return value


class RegistrationResponse(BaseModel):
    id: int
    user_name: str
    event_id: int
    status: str

    class Config:
        from_attributes = True
class EventView(BaseModel):
    id: int
    name: str
    total_seats: int
    available_seats: int
    total_registrations: int

    class Config:
        from_attributes = True