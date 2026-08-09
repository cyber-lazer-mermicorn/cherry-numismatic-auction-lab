"""
Numismatic Vision — See Coins, Grade Coins
===========================================
Photo-based coin identification and grading.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mermicorn-commerce-ai" / "src"))
from commerce_ai.vision import MermicornVision, VisionResult


class NumismaticVision:
    """
    Vision-powered coin analysis.
    
    See a coin → Identify it → Grade it → Value it
    """
    
    def __init__(self, api_key: str | None = None):
        self.vision = MermicornVision(api_key=api_key)
    
    def identify_from_photo(self, image_path: str) -> VisionResult:
        """Identify a coin from a photo."""
        return self.vision.analyze_image(image_path, task="identify")
    
    def grade_from_photo(self, image_path: str) -> VisionResult:
        """Grade a coin from a photo."""
        prompt = """Analyze this coin image for grading.

Identify:
- Coin type (date, mint mark if visible)
- Obverse condition (wear on high points)
- Reverse condition (wear on high points)
- Luster (if visible)
- Surface marks/scratches
- Eye appeal
- Overall grade estimate (Sheldon 1-70 and letter grade)

Provide JSON with:
- coin_identification: {type, year, mint_mark, denomination}
- obverse_grade: description of obverse condition
- reverse_grade: description of reverse condition
- luster_rating: 1-10
- surface_quality: 1-10
- eye_appeal: 1-10
- estimated_grade: {letter, numeric, confidence}
- key_features: list of notable features
- defects: list of any defects visible
- estimated_value_range: {low, mid, high}
- reasoning: detailed explanation"""
        
        return self.vision.analyze_image(image_path, task="grade")
    
    def compare_coins(self, image1_path: str, image2_path: str) -> VisionResult:
        """Compare two coins side by side."""
        return self.vision.compare_images(image1_path, image2_path)
    
    def get_stats(self) -> dict[str, Any]:
        return {"vision_stats": self.vision.get_stats()}
