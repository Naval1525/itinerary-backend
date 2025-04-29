from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class HotelBase(BaseModel):
    name: str
    address: Optional[str] = None
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    room_type: Optional[str] = None

class HotelCreate(HotelBase):
    pass

class Hotel(HotelBase):
    id: int
    day_id: int

    class Config:
        from_attributes = True

class TransferBase(BaseModel):
    type: str
    from_location: str
    to_location: str
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    notes: Optional[str] = None

class TransferCreate(TransferBase):
    pass

class Transfer(TransferBase):
    id: int
    day_id: int

    class Config:
        from_attributes = True

class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    cost: Optional[float] = None

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    day_id: int

    class Config:
        from_attributes = True

class DayBase(BaseModel):
    day_number: int
    date: datetime

class DayCreate(DayBase):
    hotel: Optional[HotelCreate] = None
    transfers: List[TransferCreate] = []
    activities: List[ActivityCreate] = []

class Day(DayBase):
    id: int
    trip_id: int
    hotel: Optional[Hotel] = None
    transfers: List[Transfer] = []
    activities: List[Activity] = []

    class Config:
        from_attributes = True

class TripBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime

class TripCreate(TripBase):
    days: List[DayCreate]

class Trip(TripBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    days: List[Day] = []

    class Config:
        from_attributes = True 