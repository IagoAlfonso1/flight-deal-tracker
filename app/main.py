import os
from dotenv import load_dotenv
from fastapi import FastAPI

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
