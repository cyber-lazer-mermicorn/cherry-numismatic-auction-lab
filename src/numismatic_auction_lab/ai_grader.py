"""
Numismatic AI — Coin Identification, Grading & Pricing
======================================================
Real AI-powered coin analysis.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent.parent / "mermicorn-commerce-ai" / "src"))
from commerce_ai.ai_core import MermicornAI, AIResult


@dataclass(slots=True)
class CoinAnalysis:
    """AI-powered coin analysis result."""
    name: str
    year: int | None
    mint_mark: str
    grade: str
    grade_score: int
    estimated_value: dict[str, float]  # low, mid, high
    rarity: str
    key_factors: list[str]
    confidence: float
    reasoning: str
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name, "year": self.year, "mint_mark": self.mint_mark,
            "grade": self.grade, "grade_score": self.grade_score,
            "estimated_value": self.estimated_value, "rarity": self.rarity,
            "key_factors": self.key_factors, "confidence": self.confidence,
            "reasoning": self.reasoning,
        }


class NumismaticAI:
    """
    AI-powered numismatic analysis.
    
    Capabilities:
    - Coin identification from description/photos
    - Professional grading estimation
    - Market value calculation
    - Auction listing generation
    - Portfolio analysis
    """
    
    def __init__(self, api_key: str | None = None):
        self.ai = MermicornAI(api_key=api_key)
        self.analyses: list[CoinAnalysis] = []
    
    def identify_coin(self, description: str) -> AIResult:
        """Identify a coin from description."""
        prompt = f"""Identify this coin:

{description}

Provide detailed JSON with:
- name: full coin name (e.g., "Morgan Silver Dollar")
- year: year of minting (if determinable)
- mint_mark: mint mark (P, S, D, O, CC, etc.)
- denomination: face value
- metal: composition
- weight: weight in grams
- diameter: diameter in mm
- key_features: distinctive features
- variety: variety if applicable
- error_coin: if potential error coin, describe
- confidence: 0-1"""
        
        return self.ai.analyze(prompt, task="identification")
    
    def grade_coin(self, description: str, coin_type: str = "") -> AIResult:
        """Estimate coin grade using Sheldon scale."""
        prompt = f"""Grade this {coin_type} coin:

{description}

Use the Sheldon grading scale (1-70) and letter grades:
- Poor (PO-1): 1-3
- Fair (FR-2): 4-6
- About Good (AG-3): 7-10
- Good (G-4/6): 12-20
- Very Good (VG-8/10): 25-30
- Fine (F-12/15): 35-40
- Very Fine (VF-20/25/30/35): 45-50
- Extremely Fine (EF-40/45): 55-58
- About Uncirculated (AU-50/53/55/58): 60-63
- Mint State (MS-60 to MS-70): 65-70

Provide JSON with:
- grade: letter grade (e.g., "MS-63")
- numeric_score: Sheldon score (1-70)
- eye_appeal: 1-10
- strike_quality: 1-10
- surface_preservation: 1-10
- luster: 1-10
- key_factors: list of factors affecting grade
- wear_pattern: description of wear
- confidence: 0-1
- reasoning: detailed explanation"""
        
        return self.ai.analyze(prompt, task="grading")
    
    def value_coin(self, coin_data: dict[str, Any], market_data: list[dict] | None = None) -> AIResult:
        """Calculate market value for a coin."""
        prompt = f"""Value this coin:

{json.dumps(coin_data, indent=2)}
{f"Recent sales data: {json.dumps(market_data, indent=2)}" if market_data else ""}

Consider:
- Current precious metal prices
- Numismatic premium over melt
- Grade-based value
- Market demand
- Rarity factors

Provide JSON with:
- melt_value: current metal value
- numismatic_value: collector value
- low_value: conservative estimate
- mid_value: likely retail
- high_value: premium retail
- auction_estimate: auction price range
- factors: list of value factors
- market_trend: rising/stable/declining
- confidence: 0-1"""
        
        return self.ai.analyze(prompt, task="valuation")
    
    def generate_auction_listing(self, coin_data: dict[str, Any]) -> AIResult:
        """Generate auction listing for a coin."""
        prompt = f"""Generate an auction listing for this coin:

{json.dumps(coin_data, indent=2)}

Create a compelling listing that:
- Highlights key features and rarity
- Provides accurate grading information
- Sets appropriate starting bid
- Includes shipping and return terms

Provide JSON with:
- title: auction title (max 80 chars)
- subtitle: compelling subtitle
- starting_bid: suggested starting bid
- buy_now_price: optional buy now price
- description: 200-300 word description
- highlights: 5 key selling points
- condition_note: detailed condition description
- provenance: if known
- shipping: shipping terms
- returns: return policy
- authentication: authentication guarantee"""
        
        return self.ai.analyze(prompt, task="listing")
    
    def analyze_collection(self, coins: list[dict[str, Any]]) -> AIResult:
        """Analyze a coin collection."""
        prompt = f"""Analyze this coin collection:

{json.dumps(coins, indent=2)}

Provide JSON with:
- total_coins: count
- estimated_total_value: total value estimate
- breakdown: value by type/era
- top_5_most_valuable: list of most valuable
- condition_summary: average condition
- gaps: missing coins that would complete the collection
- recommendations: suggestions for improvement
- investment_potential: assessment"""
        
        return self.ai.analyze(prompt, task="research")
    
    def get_stats(self) -> dict[str, Any]:
        return {
            "analyses_performed": len(self.analyses),
            "ai_stats": self.ai.get_stats(),
        }
