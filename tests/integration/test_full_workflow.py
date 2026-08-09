"""
Full Stack Workflow Test — Cherry Numismatic Auction Lab
========================================================
Photo → Identify → Grade → Value → Auction Listing
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, "src")
sys.path.insert(0, "../mermicorn-commerce-ai/src")
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mermicorn-commerce-ai" / "src"))

from numismatic_auction_lab.engine import NumismaticEngine
from numismatic_auction_lab.ai_grader import NumismaticAI
from numismatic_auction_lab.integrations import CoinMarketIntelligence
from numismatic_auction_lab.skills_market import NumismaticSkills


def test_full_workflow():
    """Test complete numismatic workflow: Identify → Grade → Value → List."""
    print("🪙 NUMISMATIC FULL WORKFLOW TEST")
    print("=" * 50)
    
    # ═══════════════════════════════════════════════════════════
    # STEP 1: Identify Coin (AI)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 1: Identify Coin")
    ai = NumismaticAI()
    result = ai.identify_coin("1889 Morgan Silver Dollar, appears to be in good condition with some wear on the eagle's wings")
    
    assert result.success, f"Identification failed: {result.reasoning}"
    print(f"   ✅ Identified: {result.data}")
    print(f"   ✅ Confidence: {result.confidence}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 2: Grade Coin (AI)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 2: Grade Coin")
    grade_result = ai.grade_coin("1889 Morgan Silver Dollar with moderate wear, some luster remaining on obverse", "silver dollar")
    
    assert grade_result.success, f"Grading failed: {grade_result.reasoning}"
    print(f"   ✅ Grade: {grade_result.data}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 3: Value Coin (AI)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 3: Value Coin")
    coin_data = {
        "name": "Morgan Silver Dollar",
        "year": 1889,
        "grade": "VF-30",
        "metal": "90% silver",
        "condition": "moderate wear",
    }
    value_result = ai.value_coin(coin_data)
    
    assert value_result.success, f"Valuation failed: {value_result.reasoning}"
    print(f"   ✅ Value: {value_result.data}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 4: Research Market (Integrations)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 4: Research Market")
    market = CoinMarketIntelligence()
    analysis = market.full_analysis("Morgan Dollar", "VF-30")
    
    assert "ebay_market" in analysis, "Market analysis incomplete"
    print(f"   ✅ Market analysis: {analysis['ebay_market']}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 5: Track Price (Skills)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 5: Track Price")
    skills = NumismaticSkills()
    skills.track_price("morgan_dollar", 45.0, "eBay")
    skills.track_price("morgan_dollar", 48.0, "Heritage")
    skills.track_price("morgan_dollar", 52.0, "PCGS")
    
    trend = skills.get_price_trend("morgan_dollar")
    print(f"   ✅ Price trend: {trend}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 6: Add to Watchlist
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 6: Add to Watchlist")
    skills.add_to_watchlist("Walking Liberty Half", 30.0, "high")
    skills.add_to_watchlist("Buffalo Nickel", 15.0, "medium")
    
    print(f"   ✅ Watchlist size: {len(skills.watchlist)}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 7: Generate Auction Listing (AI)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 7: Generate Auction Listing")
    auction_listing = ai.generate_auction_listing(coin_data)
    
    assert auction_listing.success, f"Auction listing failed: {auction_listing.reasoning}"
    print(f"   ✅ Auction listing: {auction_listing.data}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 8: Add to Engine
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 8: Add to Catalog")
    engine = NumismaticEngine()
    coin = engine.add_coin("Morgan Dollar", 1889, "VF-30", 52.0)
    
    assert len(engine.coins) == 1, "Coin not added"
    print(f"   ✅ Catalog: {engine.get_stats()}")
    
    # ═══════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════
    print("\n" + "=" * 50)
    print("✅ FULL WORKFLOW COMPLETE")
    print(f"   Coin: 1889 Morgan Silver Dollar")
    print(f"   Grade: VF-30")
    print(f"   Value: ~$52")
    print(f"   Market: 3 sources checked")
    print(f"   Watchlist: 2 items")
    print(f"   Catalog: {len(engine.coins)} coins")
    print("=" * 50)
    
    return True


if __name__ == "__main__":
    success = test_full_workflow()
    sys.exit(0 if success else 1)
