from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator

class FlightSearchRequest(BaseModel):
    origin: str = Field(..., min_length=3, max_length=3)
    destination: str = Field(..., min_length=3, max_length=3)

    departure_date: date = Field(..., description="YYYY-MM-DD or DD/MM/YYYY")
    return_date: date | None = Field(default=None, description="YYYY-MM-DD or DD/MM/YYYY")

    adults: int = Field(default=1, ge=1, le=9)
    non_stop: bool = Field(default=False)
    max_results: int = Field(default=10, ge=1, le=50)

    @field_validator("departure_date", "return_date", mode="before")
    @classmethod
    def parse_dates(cls, v):
        if v is None or isinstance(v, date):
            return v
        if isinstance(v, str):
            s = v.strip()
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
                try:
                    return datetime.strptime(s, fmt).date()
                except ValueError:
                    pass
        raise ValueError("Invalid date format. Use YYYY-MM-DD or DD/MM/YYYY")
