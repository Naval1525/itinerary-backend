# # from fastapi import APIRouter, Depends, HTTPException, Query
# # from sqlalchemy.orm import Session
# # from typing import List
# # from .. import schemas, models
# # from ..database import get_db

# # router = APIRouter()

# # @router.get("/recommendations/", response_model=List[schemas.Trip])
# # def get_recommendations(
# #     nights: int = Query(..., ge=1, le=30, description="Number of nights for the trip"),
# #     db: Session = Depends(get_db)
# # ):
# #     # Find trips where (end_date - start_date).days == nights
# #     trips = db.query(models.Trip).filter(
# #         (models.Trip.end_date - models.Trip.start_date).days == nights
# #     ).all()
# #     if not trips:
# #         raise HTTPException(status_code=404, detail=f"No itineraries found for {nights} nights.")
# #     return trips
# from fastapi import FastAPI, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
# from sqlalchemy import func
# from typing import List
# import uvicorn

# # Import your existing models, schemas, and db session
# from app import models, schemas
# from app.database import get_db

# app = FastAPI(title="Standalone MCP Server")

# @app.get("/recommended-itineraries/", response_model=List[schemas.Trip])
# def get_recommended_itineraries(
#     nights: int = Query(..., ge=2, le=8, description="Number of nights (2-8)"),
#     db: Session = Depends(get_db)
# ):
#     """
#     Return recommended itineraries for the given number of nights.
#     """
#     trips = db.query(models.Trip).filter(
#         func.DATE_PART('day', models.Trip.end_date - models.Trip.start_date) == nights
#     ).all()
#     if not trips:
#         raise HTTPException(status_code=404, detail=f"No itineraries found for {nights} nights.")
#     return trips

# if __name__ == "__main__":
#     uvicorn.run("mcp_server:app", host="0.0.0.0", port=8000, reload=True)
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import os
import httpx
from .. import schemas, models
from ..database import get_db

router = APIRouter()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def format_itineraries(itineraries):
    # Convert your DB objects to a readable string for Gemini
    result = []
    for trip in itineraries:
        days = []
        for day in trip.days:
            day_str = f"Day {day.day_number}: {day.date.date()}"
            if day.hotel:
                day_str += f", Hotel: {day.hotel.name}"
            if day.activities:
                acts = "; ".join(a.title for a in day.activities)
                day_str += f", Activities: {acts}"
            if day.transfers:
                trans = "; ".join(f"{t.type} from {t.from_location} to {t.to_location}" for t in day.transfers)
                day_str += f", Transfers: {trans}"
            days.append(day_str)
        trip_str = f"Trip: {trip.title} ({(trip.end_date - trip.start_date).days} nights)\n" + "\n".join(days)
        result.append(trip_str)
    return "\n\n".join(result)

@router.get("/gemini-recommendation/")
async def gemini_recommendation(
    nights: int = Query(..., ge=2, le=8, description="Number of nights (2-8)"),
    region: Optional[str] = Query(None, description="Region (Phuket or Krabi)"),
    db: Session = Depends(get_db)
):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set in environment.")

    # Query DB for matching itineraries
    query = db.query(models.Trip).filter(
        func.DATE_PART('day', models.Trip.end_date - models.Trip.start_date) == nights
    )
    if region:
        query = query.filter(models.Trip.title.ilike(f"%{region}%"))
    trips = query.all()
    if not trips:
        raise HTTPException(status_code=404, detail=f"No itineraries found for {nights} nights.")

    # Format itineraries for Gemini
    trips_text = format_itineraries(trips)
    prompt = (
        f"Here are some itineraries for {nights} nights"
        + (f" in {region}" if region else "")
        + ":\n\n"
        + trips_text
        + "\n\nBased on these, which would you recommend to a traveler and why? Respond with the best option and a short explanation."
    )

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            GEMINI_URL,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Gemini API error: {response.text}")
        data = response.json()
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            text = data
        return {"gemini_recommendation": text}