import os
import requests
from fastapi import FastAPI, Query
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running!"}

@app.get("/nearby-medical-stores/")
def find_stores(lat: float = Query(...), lon: float = Query(...)):
    """
    Find nearby medical stores using Overpass API (OpenStreetMap).
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node["amenity"="pharmacy"](around:5000,{lat},{lon});
    out;
    """
    
    print("📡 Sending Overpass API Request...")
    print("🔍 Query:", query)

    response = requests.get(overpass_url, params={"data": query})
    
    if response.status_code != 200:
        print("❌ Overpass API Error:", response.text)
        return {"error": "Failed to fetch data from Overpass API"}

    data = response.json()
    
    print("✅ Overpass API Response:", data)  # Debug Response

    stores = [
        {
            "name": element.get("tags", {}).get("name", "Unknown Pharmacy"),
            "latitude": element["lat"],
            "longitude": element["lon"],
        }
        for element in data.get("elements", [])
    ]

    print("📌 Final Data Sent to Client:", stores)  # Debug Output
    return {"medical_stores": stores}




