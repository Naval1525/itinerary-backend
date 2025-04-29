from fastapi import FastAPI
from .routes import itinerary
from .database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Itinerary Manager API",
    description="API for managing travel itineraries with day-wise details",
    version="1.0.0"
)

app.include_router(itinerary.router, prefix="/api/v1", tags=["itineraries"]) 