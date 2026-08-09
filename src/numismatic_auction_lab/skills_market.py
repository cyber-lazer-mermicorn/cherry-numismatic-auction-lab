"""
Numismatic Skills — Coin Market Intelligence
=============================================
Specialized skills for numismatic research.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mermicorn-commerce-ai" / "src"))
from commerce_ai.skills import MermicornSkills, DataAnalysisSkill


class NumismaticSkills:
    """
    Specialized numismatic skills.
    
    Provides:
    - Price tracking and trends
    - Auction monitoring
    - Portfolio analytics
    - Market intelligence
    - Deal alerts
    """
    
    def __init__(self, storage_dir: str = "./numismatic_data"):
        self.skills = MermicornSkills(storage_dir)
        self.price_history: dict[str, list[dict]] = {}
        self.watchlist: list[dict] = []
    
    def track_price(self, coin_id: str, price: float, source: str = "manual") -> None:
        """Track a coin's price over time."""
        self.skills.data.add_point(f"price:{coin_id}", price, source)
        
        if coin_id not in self.price_history:
            self.price_history[coin_id] = []
        self.price_history[coin_id].append({
            "price": price, "source": source, "timestamp": time.time(),
        })
    
    def get_price_trend(self, coin_id: str) -> dict[str, Any]:
        """Get price trend for a coin."""
        return self.skills.data.summary(f"price:{coin_id}")
    
    def add_to_watchlist(self, coin_name: str, target_price: float,
                        priority: str = "medium") -> None:
        """Add coin to watchlist."""
        self.watchlist.append({
            "name": coin_name, "target_price": target_price,
            "priority": priority, "added": time.time(),
        })
        self.skills.memory.remember(
            f"watchlist:{coin_name}",
            {"target": target_price, "priority": priority},
            category="watchlist",
            importance=0.7,
        )
    
    def check_deals(self, current_prices: dict[str, float]) -> list[dict[str, Any]]:
        """Check for deals below target price."""
        deals = []
        for item in self.watchlist:
            name = item["name"]
            if name in current_prices and current_prices[name] < item["target_price"]:
                savings = item["target_price"] - current_prices[name]
                deals.append({
                    "name": name, "current": current_prices[name],
                    "target": item["target_price"], "savings": savings,
                    "discount_pct": savings / item["target_price"] * 100,
                })
        return sorted(deals, key=lambda d: d["discount_pct"], reverse=True)
    
    def analyze_portfolio(self, portfolio: list[dict[str, Any]]) -> dict[str, Any]:
        """Analyze a coin portfolio."""
        total_value = sum(c.get("value", 0) for c in portfolio)
        total_cost = sum(c.get("cost", c.get("value", 0)) for c in portfolio)
        
        return {
            "total_value": total_value,
            "total_cost": total_cost,
            "profit_loss": total_value - total_cost,
            "roi_pct": (total_value - total_cost) / max(total_cost, 1) * 100,
            "coin_count": len(portfolio),
            "avg_value": total_value / max(len(portfolio), 1),
        }
    
    def market_intelligence(self, coin_type: str) -> dict[str, Any]:
        """Get market intelligence for a coin type."""
        trend = self.skills.data.summary(f"price:{coin_type}")
        memory = self.skills.memory.search(coin_type, category="market")
        
        return {
            "coin_type": coin_type,
            "trend": trend,
            "recent_notes": [m.value for m in memory[:5]],
            "recommendation": self._recommend(trend),
        }
    
    def _recommend(self, trend: dict) -> str:
        """Generate recommendation based on trend."""
        if trend.get("count", 0) < 2:
            return "Need more data"
        if trend.get("trend") == "rising":
            return "Consider selling"
        elif trend.get("trend") == "falling":
            return "Good buying opportunity"
        return "Hold"
    
    def get_stats(self) -> dict[str, Any]:
        return {
            "skills": self.skills.get_stats(),
            "tracked_coins": len(self.price_history),
            "watchlist_size": len(self.watchlist),
        }
