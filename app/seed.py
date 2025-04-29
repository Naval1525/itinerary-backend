from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models

def seed_database(db: Session):
    # Phuket 5-day itinerary
    phuket_trip = models.Trip(
        title="Phuket Paradise Getaway",
        description="5-day luxury vacation in Phuket",
        start_date=datetime.now() + timedelta(days=30),
        end_date=datetime.now() + timedelta(days=35)
    )
    db.add(phuket_trip)
    db.flush()

    # Day 1 - Arrival
    day1 = models.Day(
        trip_id=phuket_trip.id,
        day_number=1,
        date=phuket_trip.start_date
    )
    db.add(day1)
    db.flush()

    hotel1 = models.Hotel(
        day_id=day1.id,
        name="The Nai Harn",
        address="Nai Harn Beach, Phuket",
        check_in=datetime.now() + timedelta(days=30, hours=14),
        check_out=datetime.now() + timedelta(days=31, hours=12),
        room_type="Deluxe Ocean View"
    )
    db.add(hotel1)

    transfer1 = models.Transfer(
        day_id=day1.id,
        type="airport",
        from_location="Phuket International Airport",
        to_location="The Nai Harn",
        departure_time=datetime.now() + timedelta(days=30, hours=13),
        arrival_time=datetime.now() + timedelta(days=30, hours=14)
    )
    db.add(transfer1)

    # Day 2 - Island Hopping
    day2 = models.Day(
        trip_id=phuket_trip.id,
        day_number=2,
        date=phuket_trip.start_date + timedelta(days=1)
    )
    db.add(day2)
    db.flush()

    activity1 = models.Activity(
        day_id=day2.id,
        title="Phi Phi Islands Tour",
        description="Full-day boat tour to Phi Phi Islands",
        start_time=datetime.now() + timedelta(days=31, hours=8),
        end_time=datetime.now() + timedelta(days=31, hours=17),
        location="Phi Phi Islands",
        cost=150.00
    )
    db.add(activity1)

    # Krabi 4-day itinerary
    krabi_trip = models.Trip(
        title="Krabi Adventure",
        description="4-day adventure in Krabi",
        start_date=datetime.now() + timedelta(days=45),
        end_date=datetime.now() + timedelta(days=49)
    )
    db.add(krabi_trip)
    db.flush()

    # Day 1 - Arrival
    krabi_day1 = models.Day(
        trip_id=krabi_trip.id,
        day_number=1,
        date=krabi_trip.start_date
    )
    db.add(krabi_day1)
    db.flush()

    krabi_hotel1 = models.Hotel(
        day_id=krabi_day1.id,
        name="Rayavadee",
        address="Railay Beach, Krabi",
        check_in=datetime.now() + timedelta(days=45, hours=14),
        check_out=datetime.now() + timedelta(days=46, hours=12),
        room_type="Garden Pavilion"
    )
    db.add(krabi_hotel1)

    krabi_transfer1 = models.Transfer(
        day_id=krabi_day1.id,
        type="airport",
        from_location="Krabi International Airport",
        to_location="Rayavadee",
        departure_time=datetime.now() + timedelta(days=45, hours=13),
        arrival_time=datetime.now() + timedelta(days=45, hours=14)
    )
    db.add(krabi_transfer1)

    # Day 2 - Rock Climbing
    krabi_day2 = models.Day(
        trip_id=krabi_trip.id,
        day_number=2,
        date=krabi_trip.start_date + timedelta(days=1)
    )
    db.add(krabi_day2)
    db.flush()

    krabi_activity1 = models.Activity(
        day_id=krabi_day2.id,
        title="Railay Beach Rock Climbing",
        description="Half-day rock climbing session",
        start_time=datetime.now() + timedelta(days=46, hours=9),
        end_time=datetime.now() + timedelta(days=46, hours=13),
        location="Railay Beach",
        cost=75.00
    )
    db.add(krabi_activity1)

    db.commit() 