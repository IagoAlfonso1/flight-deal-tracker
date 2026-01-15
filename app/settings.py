import os
from dotenv import load_dotenv

load_dotenv()

def get_env(name: str) -> str:
    return os.getenv(name, "").strip()

AMADEUS_CLIENT_ID = get_env("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = get_env("AMADEUS_CLIENT_SECRET")
