from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routes import events
from app.routes import registrations
from app.config import APP_NAME, APP_VERSION
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

app.include_router(events.router)
app.include_router(registrations.router)

@app.get("/")
def home():
    return {"message": "API Running"}