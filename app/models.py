from pydantic import BaseModel, Field

class FlightSearchRequest(BaseModel):
    origin: str = Field(..., min_length=3, max_length=3, description="IATA origin (e.g., EZE)")
    destination: str = Field(..., min_length=3, max_length=3, description="IATA destination (e.g., BCN)")
    departure_date: str = Field(..., description="YYYY-MM-DD")
    return_date: str | None = Field(default=None, description="YYYY-MM-DD (optional)")
    adults: int = Field(default=1, ge=1, le=9)
