from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base
from app.config import EVENTS_TABLE, REGISTRATIONS_TABLE

class Event(Base):
    __tablename__ = EVENTS_TABLE

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    total_seats = Column(Integer, nullable=False)
    event_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Registration(Base):
    __tablename__ = REGISTRATIONS_TABLE

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    registered_at = Column(DateTime, server_default=func.now())
    status = Column(String, default="ACTIVE")
    __table_args__ = (
    UniqueConstraint("user_name", "event_id", "status", name="unique_active_registration"),
)