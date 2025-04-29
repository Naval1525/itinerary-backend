from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import schemas, models
from ..database import get_db

router = APIRouter()

# MCP endpoint: recommended itineraries by nights and optional region
@router.get("/recommendations/", response_model=List[schemas.Trip])
def get_recommended_itineraries(
    nights: int = Query(..., ge=2, le=8, description="Number of nights (2-8)"),
    region: Optional[str] = Query(None, description="Optional region filter (e.g., Phuket, Krabi)"),
    db: Session = Depends(get_db)
):
    """
    Get recommended itineraries based on number of nights and optional region.
    """
    # Calculate duration in days (nights)
    query = db.query(models.Trip).filter(
        func.DATE_PART('day', models.Trip.end_date - models.Trip.start_date) == nights
    )
    if region:
        query = query.filter(models.Trip.title.ilike(f"%{region}%"))
    trips = query.all()
    if not trips:
        msg = f"No recommended itineraries found for {nights} nights"
        if region:
            msg += f" in {region}"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
    return trips

# Endpoint: available regions (from trip titles)
@router.get("/available-regions", response_model=List[str])
def get_available_regions(db: Session = Depends(get_db)):
    """
    Get list of available regions for itineraries (from trip titles).
    """
    regions = db.query(models.Trip.title).all()
    # Extract region names from titles (e.g., "Phuket Paradise Getaway" -> "Phuket")
    region_names = set()
    for (title,) in regions:
        if "Phuket" in title:
            region_names.add("Phuket")
        if "Krabi" in title:
            region_names.add("Krabi")
    return list(region_names)

# Endpoint: get itinerary by ID
@router.get("/itinerary/{trip_id}", response_model=schemas.Trip)
def get_itinerary_by_id(trip_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific itinerary.
    """
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Itinerary with ID {trip_id} not found"
        )
    return trip
