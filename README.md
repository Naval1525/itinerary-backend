# Itinerary Manager API

A FastAPI-based backend for managing travel itineraries with day-wise details including hotels, transfers, and activities.

## Features

- Create and manage travel itineraries
- Add day-wise details including:
  - Hotels
  - Transfers
  - Activities
- Sample itineraries for Phuket and Krabi

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the database:
- Create a PostgreSQL database named `itinerary_db`
- Update the DATABASE_URL in `.env` file:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/itinerary_db
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

**Base URL:**  
`http://localhost:8000/api/v1`

- **Create a new itinerary (POST):**  
  `http://localhost:8000/api/v1/itineraries/`
- **Get all itineraries (GET):**  
  `http://localhost:8000/api/v1/itineraries/`
- **Get a specific itinerary by ID (GET):**  
  `http://localhost:8000/api/v1/itineraries/{trip_id}`
- **Recommended itineraries from the database for a given number of nights (GET):**  
  `http://localhost:8000/api/v1/mcp/recommended-itineraries/?nights={nights}`


**Interactive API Docs:**  
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## API Documentation

### POST `/api/v1/itineraries/`

**Create a new itinerary**

**Sample Request:**
```json
{
  "title": "Bali Adventure",
  "description": "7-day trip to Bali",
  "start_date": "2024-06-01T00:00:00",
  "end_date": "2024-06-08T00:00:00",
  "days": [
    {
      "day_number": 1,
      "date": "2024-06-01T00:00:00",
      "hotel": {
        "name": "The Mulia",
        "address": "Nusa Dua, Bali",
        "check_in": "2024-06-01T14:00:00",
        "check_out": "2024-06-02T12:00:00",
        "room_type": "Ocean Suite"
      },
      "transfers": [
        {
          "type": "airport",
          "from_location": "Ngurah Rai Airport",
          "to_location": "The Mulia",
          "departure_time": "2024-06-01T13:00:00",
          "arrival_time": "2024-06-01T14:00:00"
        }
      ],
      "activities": [
        {
          "title": "Welcome Dinner",
          "description": "Traditional Balinese dinner",
          "start_time": "2024-06-01T19:00:00",
          "end_time": "2024-06-01T22:00:00",
          "location": "The Mulia Restaurant",
          "cost": 75.00
        }
      ]
    }
  ]
}
```

**Sample Response:**
```json
{
  "id": 1,
  "title": "Bali Adventure",
  "description": "7-day trip to Bali",
  "start_date": "2024-06-01T00:00:00",
  "end_date": "2024-06-08T00:00:00",
  "created_at": "2024-05-01T12:00:00",
  "updated_at": null,
  "days": [
    {
      "id": 1,
      "trip_id": 1,
      "day_number": 1,
      "date": "2024-06-01T00:00:00",
      "hotel": {
        "id": 1,
        "day_id": 1,
        "name": "The Mulia",
        "address": "Nusa Dua, Bali",
        "check_in": "2024-06-01T14:00:00",
        "check_out": "2024-06-02T12:00:00",
        "room_type": "Ocean Suite"
      },
      "transfers": [
        {
          "id": 1,
          "day_id": 1,
          "type": "airport",
          "from_location": "Ngurah Rai Airport",
          "to_location": "The Mulia",
          "departure_time": "2024-06-01T13:00:00",
          "arrival_time": "2024-06-01T14:00:00",
          "notes": null
        }
      ],
      "activities": [
        {
          "id": 1,
          "day_id": 1,
          "title": "Welcome Dinner",
          "description": "Traditional Balinese dinner",
          "start_time": "2024-06-01T19:00:00",
          "end_time": "2024-06-01T22:00:00",
          "location": "The Mulia Restaurant",
          "cost": 75.0
        }
      ]
    }
  ]
}
```

---

### GET `/api/v1/itineraries/`

**Get all itineraries**

**Sample Response:**
```json
[
  {
    "id": 1,
    "title": "Bali Adventure",
    "description": "7-day trip to Bali",
    "start_date": "2024-06-01T00:00:00",
    "end_date": "2024-06-08T00:00:00",
    "created_at": "2024-05-01T12:00:00",
    "updated_at": null,
    "days": [
      {
        "id": 1,
        "trip_id": 1,
        "day_number": 1,
        "date": "2024-06-01T00:00:00",
        "hotel": {
          "id": 1,
          "day_id": 1,
          "name": "The Mulia",
          "address": "Nusa Dua, Bali",
          "check_in": "2024-06-01T14:00:00",
          "check_out": "2024-06-02T12:00:00",
          "room_type": "Ocean Suite"
        },
        "transfers": [
          {
            "id": 1,
            "day_id": 1,
            "type": "airport",
            "from_location": "Ngurah Rai Airport",
            "to_location": "The Mulia",
            "departure_time": "2024-06-01T13:00:00",
            "arrival_time": "2024-06-01T14:00:00",
            "notes": null
          }
        ],
        "activities": [
          {
            "id": 1,
            "day_id": 1,
            "title": "Welcome Dinner",
            "description": "Traditional Balinese dinner",
            "start_time": "2024-06-01T19:00:00",
            "end_time": "2024-06-01T22:00:00",
            "location": "The Mulia Restaurant",
            "cost": 75.0
          }
        ]
      }
    ]
  }
]
```

---

### GET `/api/v1/itineraries/{trip_id}`

**Get a specific itinerary by ID**

**Sample Response:**
```json
{
  "id": 1,
  "title": "Bali Adventure",
  "description": "7-day trip to Bali",
  "start_date": "2024-06-01T00:00:00",
  "end_date": "2024-06-08T00:00:00",
  "created_at": "2024-05-01T12:00:00",
  "updated_at": null,
  "days": [
    {
      "id": 1,
      "trip_id": 1,
      "day_number": 1,
      "date": "2024-06-01T00:00:00",
      "hotel": {
        "id": 1,
        "day_id": 1,
        "name": "The Mulia",
        "address": "Nusa Dua, Bali",
        "check_in": "2024-06-01T14:00:00",
        "check_out": "2024-06-02T12:00:00",
        "room_type": "Ocean Suite"
      },
      "transfers": [
        {
          "id": 1,
          "day_id": 1,
          "type": "airport",
          "from_location": "Ngurah Rai Airport",
          "to_location": "The Mulia",
          "departure_time": "2024-06-01T13:00:00",
          "arrival_time": "2024-06-01T14:00:00",
          "notes": null
        }
      ],
      "activities": [
        {
          "id": 1,
          "day_id": 1,
          "title": "Welcome Dinner",
          "description": "Traditional Balinese dinner",
          "start_time": "2024-06-01T19:00:00",
          "end_time": "2024-06-01T22:00:00",
          "location": "The Mulia Restaurant",
          "cost": 75.0
        }
      ]
    }
  ]
}
```

---


### GET  `/api/v1/mcp/recommended-itineraries/`

**Recommendation**


**Sample Response:**
```json
{
  "gemini_recommendation": "I recommend the 'Phuket Paradise Getaway' itinerary for 4 nights in Phuket because it offers a great mix of relaxation and adventure, including a luxury hotel stay and a Phi Phi Islands tour."
}
```

---

## Database Schema

The application uses the following main tables:
- `trips` - Main trip information
- `days` - Day-wise details
- `hotels` - Hotel information
- `transfers` - Transfer information
- `activities` - Activity information

## License

MIT License

Copyright (c) 2024 Naval Bihani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 