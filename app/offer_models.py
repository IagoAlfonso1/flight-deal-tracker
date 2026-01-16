from pydantic import BaseModel
from typing import List

class OfferSummary(BaseModel):
    id: str
    price_total: float
    currency: str
    airlines: List[str]
    outbound_from: str
    outbound_to: str
    outbound_departure: str
    outbound_arrival: str
    outbound_stops: int
    duration: str  # ejemplo: "PT12H30M"
