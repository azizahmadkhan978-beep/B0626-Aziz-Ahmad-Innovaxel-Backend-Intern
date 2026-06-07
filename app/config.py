from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./events.db")

APP_NAME = os.getenv("APP_NAME", "Event Registration System API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "True") == "True"

EVENTS_TABLE = os.getenv("EVENTS_TABLE", "events")
REGISTRATIONS_TABLE = os.getenv("REGISTRATIONS_TABLE", "registrations")

DEFAULT_REGISTRATION_STATUS = os.getenv("DEFAULT_REGISTRATION_STATUS", "ACTIVE")
CANCELLED_REGISTRATION_STATUS = os.getenv("CANCELLED_REGISTRATION_STATUS", "CANCELLED")