from typing import List
from app.offer_models import OfferSummary

def _to_float(x) -> float:
    try:
        return float(x)
    except Exception:
        return 0.0

def summarize_offers(amadeus_json: dict) -> List[OfferSummary]:
    offers = []
    data = amadeus_json.get("data", []) or []

    for item in data:
        offer_id = item.get("id", "")
        price = item.get("price", {})
        total = _to_float(price.get("total"))
        currency = price.get("currency", "USD")

        itineraries = item.get("itineraries", []) or []
        if not itineraries:
            continue

        out_it = itineraries[0]
        segments = out_it.get("segments", []) or []
        if not segments:
            continue

        first = segments[0]
        last = segments[-1]

        outbound_from = first.get("departure", {}).get("iataCode", "")
        outbound_to = last.get("arrival", {}).get("iataCode", "")
        outbound_departure = first.get("departure", {}).get("at", "")
        outbound_arrival = last.get("arrival", {}).get("at", "")
        outbound_stops = max(len(segments) - 1, 0)
        duration = out_it.get("duration", "")

        airlines = sorted({seg.get("carrierCode", "") for seg in segments if seg.get("carrierCode")})

        offers.append(
            OfferSummary(
                id=offer_id,
                price_total=total,
                currency=currency,
                airlines=airlines,
                outbound_from=outbound_from,
                outbound_to=outbound_to,
                outbound_departure=outbound_departure,
                outbound_arrival=outbound_arrival,
                outbound_stops=outbound_stops,
                duration=duration,
            )
        )

    offers.sort(key=lambda o: o.price_total)
    return offers
