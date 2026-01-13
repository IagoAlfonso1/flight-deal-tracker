import os
import requests

AMADEUS_TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"

def has_amadeus_config() -> bool:
    client_id = os.getenv("AMADEUS_CLIENT_ID", "").strip()
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET", "").strip()
    return bool(client_id) and bool(client_secret)

def get_access_token() -> str:
    """
    Devuelve access token usando el entorno TEST de Amadeus.
    Requiere AMADEUS_CLIENT_ID y AMADEUS_CLIENT_SECRET en el entorno.
    """
    client_id = os.getenv("AMADEUS_CLIENT_ID", "").strip()
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET", "").strip()

    if not client_id or not client_secret:
        raise RuntimeError("Missing Amadeus credentials (set AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET).")

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    r = requests.post(AMADEUS_TOKEN_URL, data=data, timeout=20)
    r.raise_for_status()
    token = r.json().get("access_token")
    if not token:
        raise RuntimeError("No access_token in response.")
    return token
