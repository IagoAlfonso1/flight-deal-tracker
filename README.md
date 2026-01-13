#Flight Deal Tracker

Backend en Python (FastAPI) para consultar precios de vuelos y guardar histórico para detectar ofertas.

## Stack
- Python
- FastAPI
- Uvicorn

## Requisitos
- Python 3.10+

## Setup
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

## Environment variables
Create a local `.env` file (do NOT commit it) with:

```env
AMADEUS_CLIENT_ID=your_id
AMADEUS_CLIENT_SECRET=your_secret