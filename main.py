import os
import requests
from fastapi import FastAPI, Query
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

@app.get("/")
def home(lat: float = Query(28.7041), lon: float = Query(77.1025)):
    """
    Homepage that also shows nearby medical stores.
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node["amenity"="pharmacy"](around:5000,{lat},{lon});
    out;
    """
    response = requests.get(overpass_url, params={"data": query})

    if response.status_code != 200:
        return {"error": "Failed to fetch data from Overpass API"}

    data = response.json()
    
    stores = [
        {
            "name": element.get("tags", {}).get("name", "Unknown Pharmacy"),
            "latitude": element["lat"],
            "longitude": element["lon"],
        }
        for element in data.get("elements", [])
    ]

    return {
        "message": "Welcome to the Nearby Medical Store Finder API!",
        "stores": stores
    }


@app.get("/nearby-medical-stores/")
def find_stores(lat: float = Query(...), lon: float = Query(...)):
    """
    Find nearby medical stores using the Overpass API (OpenStreetMap).
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node["amenity"="pharmacy"](around:5000,{lat},{lon});
    out;
    """
    
    response = requests.get(overpass_url, params={"data": query})
    
    if response.status_code != 200:
        return {"error": "Failed to fetch data from Overpass API"}

    data = response.json()
    
    stores = [
        {
            "name": element.get("tags", {}).get("name", "Unknown Pharmacy"),
            "latitude": element["lat"],
            "longitude": element["lon"],
        }
        for element in data.get("elements", [])
    ]

    return {"medical_stores": stores}
