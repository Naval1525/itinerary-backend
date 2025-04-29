from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    days = relationship("Day", back_populates="trip", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_trip_dates', 'start_date', 'end_date'),
    )

class Day(Base):
    __tablename__ = "days"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    day_number = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    
    trip = relationship("Trip", back_populates="days")
    hotel = relationship("Hotel", back_populates="day", uselist=False, cascade="all, delete-orphan")
    transfers = relationship("Transfer", back_populates="day", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="day", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_day_trip_date', 'trip_id', 'date'),
    )

class Hotel(Base):
    __tablename__ = "hotels"
    
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(Text)
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    room_type = Column(String(100))
    
    day = relationship("Day", back_populates="hotel")

class Transfer(Base):
    __tablename__ = "transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)  # e.g., "airport", "hotel", "activity"
    from_location = Column(String(255), nullable=False)
    to_location = Column(String(255), nullable=False)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    notes = Column(Text)
    
    day = relationship("Day", back_populates="transfers")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String(255))
    cost = Column(Float)
    
    day = relationship("Day", back_populates="activities") 