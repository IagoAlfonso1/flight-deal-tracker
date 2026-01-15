import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.amadeus_client import has_amadeus_config, get_access_token
from app.models import FlightSearchRequest



# Carga variables desde .env si existe (en local)
load_dotenv()

app = FastAPI(title="Flight Deal Tracker")

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
    # Por ahora: stub para validar input + dejar listo el contrato
    return {
        "ok": True,
        "message": "search endpoint ready (stub)",
        "request": payload.model_dump(),
        "next": "Tomorrow: call Amadeus API and return real offers"
    }
