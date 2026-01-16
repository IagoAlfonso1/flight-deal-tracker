import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.amadeus_client import has_amadeus_config,search_flight_offers
from app.models import FlightSearchRequest
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.normalizers import summarize_offers


# Carga variables desde .env si existe (en local)
load_dotenv()

app = FastAPI(title="Flight Deal Tracker")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/config-check")
def config_check():
    client_id = os.getenv("AMADEUS_CLIENT_ID", "").strip()
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET", "").strip()

    configured = bool(client_id) and bool(client_secret)
    return {"amadeus_configured": configured}

@app.get("/amadeus/token-status")
def amadeus_token_status():
    if not has_amadeus_config():
        return {"ok": False, "reason": "missing_amadeus_credentials"}

    try:
        token = get_access_token()
        return {"ok": True, "token_preview": token[:10] + "..."}
    except Exception as e:
        return {"ok": False, "reason": str(e)}

@app.post("/flights/search")
def flights_search(payload: FlightSearchRequest):
    if not has_amadeus_config():
        return {
            "ok": False,
            "reason": "missing_amadeus_credentials",
            "request": payload.model_dump(),
            "hint": "Create a local .env using .env.example (do not commit secrets)."
        }

    try:
        data = search_flight_offers(
            origin=payload.origin,
            destination=payload.destination,
            departure_date=payload.departure_date.isoformat(),
            return_date=payload.return_date.isoformat() if payload.return_date else None,
            adults=payload.adults,
            non_stop=payload.non_stop,
            max_results=payload.max_results,
        )
        return {"ok": True, "data": data}
    except Exception as e:
        # no filtramos tokens/secret; devolvemos error genérico
        return {"ok": False, "reason": "amadeus_request_failed", "detail": str(e)}


@app.get("/flights/search/example")
def flights_search_example():
    return {
        "origin": "EZE",
        "destination": "BCN",
        "departure_date": "2026-02-10",
        "return_date": "2026-02-25",
        "adults": 1
    }

@app.post("/flights/search/summary")
def flights_search_summary(payload: FlightSearchRequest):
    if not has_amadeus_config():
        return {"ok": False, "reason": "missing_amadeus_credentials"}

    try:
        raw = search_flight_offers(
            origin=payload.origin,
            destination=payload.destination,
            departure_date=payload.departure_date.isoformat(),
            return_date=payload.return_date.isoformat() if payload.return_date else None,
            adults=payload.adults,
            non_stop=payload.non_stop,
            max_results=payload.max_results,
        )
        offers = summarize_offers(raw)
        return {"ok": True, "offers": [o.model_dump() for o in offers]}
    except Exception as e:
        return {"ok": False, "reason": "amadeus_request_failed", "detail": str(e)}
