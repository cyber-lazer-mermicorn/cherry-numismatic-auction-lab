"""
Numismatic Auction Lab — Platform Integration
===============================================
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "mermicorn-client"))

from mermicorn_client import MermicornClient


def get_client() -> MermicornClient:
    return MermicornClient(
        api_url=os.environ.get("MERMICORN_API_URL", "http://localhost:8000"),
        api_key=os.environ.get("MERMICORN_API_KEY", ""),
    )


def sync_coins(coins: list[dict]) -> dict:
    """Sync coin collection to central platform."""
    client = get_client()
    results = []
    for c in coins:
        result = client.coins.add(
            name=c["name"], year=c["year"],
            grade=c["grade"], price=c["price"],
        )
        results.append(result)
    return {"synced": len(results), "results": results}
