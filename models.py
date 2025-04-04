from pydantic import BaseModel

class Store(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
