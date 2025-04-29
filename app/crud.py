from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def create_trip(db: Session, trip: schemas.TripCreate):
    db_trip = models.Trip(
        title=trip.title,
        description=trip.description,
        start_date=trip.start_date,
        end_date=trip.end_date
    )
    db.add(db_trip)
    db.flush()  # Get the trip ID without committing

    for day_data in trip.days:
        db_day = models.Day(
            trip_id=db_trip.id,
            day_number=day_data.day_number,
            date=day_data.date
        )
        db.add(db_day)
        db.flush()

        if day_data.hotel:
            db_hotel = models.Hotel(
                day_id=db_day.id,
                **day_data.hotel.model_dump()
            )
            db.add(db_hotel)

        for transfer_data in day_data.transfers:
            db_transfer = models.Transfer(
                day_id=db_day.id,
                **transfer_data.model_dump()
            )
            db.add(db_transfer)

        for activity_data in day_data.activities:
            db_activity = models.Activity(
                day_id=db_day.id,
                **activity_data.model_dump()
            )
            db.add(db_activity)

    db.commit()
    db.refresh(db_trip)
    return db_trip

def get_trips(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trip).offset(skip).limit(limit).all()

def get_trip(db: Session, trip_id: int):
    return db.query(models.Trip).filter(models.Trip.id == trip_id).first() 