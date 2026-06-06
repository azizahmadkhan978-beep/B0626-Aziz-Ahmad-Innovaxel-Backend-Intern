# B0626-Aziz-Ahmad-Innovaxel-Backend-Intern
Event Registration System API built using FastAPI and SQLite for Innovaxel Backend Internship Assessment.
# Event Registration System API

Backend internship assessment submission for Innovaxel.

## Features

* Create Events
* Register Users for Events
* View Events
* Cancel Registrations
* Event Filtering
* Event Sorting
* Input Validation
* Race Condition Handling

## Tech Stack

* Python
* FastAPI
* SQLite
* SQLAlchemy
* Pytest

## Project Structure

app/

* main.py
* database.py
* models.py
* schemas.py
* services.py
* routes/

tests/

## How to Run

1. Install dependencies
2. Start the FastAPI server
3. Open Swagger documentation

## API Endpoints

### Events

* POST /events
* GET /events

### Registrations

* POST /register
* DELETE /register/{id}

## Author

Aziz Ahmad
