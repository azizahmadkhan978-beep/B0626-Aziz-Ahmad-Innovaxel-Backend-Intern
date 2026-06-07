import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API Running"}


def test_create_event():
    unique_name = f"Test Event {uuid.uuid4()}"
    
    response = client.post("/events", json={
        "name": unique_name,
        "total_seats": 5,
        "event_date": "2026-09-01T10:00:00"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == unique_name
    assert data["total_seats"] == 5


def test_duplicate_event():
    unique_name = f"Duplicate Event {uuid.uuid4()}"
    client.post("/events", json={
        "name": unique_name,
        "total_seats": 5,
        "event_date": "2026-09-01T10:00:00"
    })

    response = client.post("/events", json={
        "name": unique_name,
        "total_seats": 5,
        "event_date": "2026-09-01T10:00:00"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Event name already exists"


def test_register_user():
    unique_event_name = f"Register Event {uuid.uuid4()}"
    event_response = client.post("/events", json={
        "name": unique_event_name,
        "total_seats": 2,
        "event_date": "2026-09-01T10:00:00"
    })
    assert event_response.status_code == 200
    event_id = event_response.json()["id"]

    response = client.post("/register", json={
        "user_name": "Aziz",
        "event_id": event_id
    })

    assert response.status_code == 200
    assert response.json()["user_name"] == "Aziz"
    assert response.json()["status"] == "ACTIVE"


def test_event_full():
    unique_event_name = f"Full Event {uuid.uuid4()}"
    event_response = client.post("/events", json={
        "name": unique_event_name,
        "total_seats": 1,
        "event_date": "2026-09-01T10:00:00"
    })
    assert event_response.status_code == 200
    event_id = event_response.json()["id"]

    client.post("/register", json={
        "user_name": "Aziz",
        "event_id": event_id
    })

    response = client.post("/register", json={
        "user_name": "Ali",
        "event_id": event_id
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Event is full"
