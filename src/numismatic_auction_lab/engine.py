"""Cherry Numismatic Auction Lab — Coin Catalog & Pricing Engine."""

from __future__ import annotations
import json, time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Coin:
    name: str
    year: int
    grade: str
    price: float
    variety: str = ""
    source: str = ""
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "year": self.year, "grade": self.grade,
                "price": self.price, "variety": self.variety, "tags": self.tags}


class NumismaticEngine:
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.coins: list[Coin] = []

    def add_coin(self, name: str, year: int, grade: str, price: float, **kw) -> Coin:
        coin = Coin(name=name, year=year, grade=grade, price=price, **kw)
        self.coins.append(coin)
        return coin

    def search(self, query: str) -> list[Coin]:
        q = query.lower()
        return [c for c in self.coins if q in c.name.lower() or q in c.grade.lower()]

    def export(self) -> str:
        path = self.output_dir / "catalog.json"
        path.write_text(json.dumps([c.to_dict() for c in self.coins], indent=2))
        return str(path)

    def get_stats(self) -> dict[str, Any]:
        return {"total": len(self.coins), "avg_price": sum(c.price for c in self.coins) / max(len(self.coins), 1)}
