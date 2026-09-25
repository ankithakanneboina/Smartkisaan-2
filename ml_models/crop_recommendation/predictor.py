"""
Rule-based crop recommendation scorer.

This is intentionally NOT a trained ML model — it's a transparent,
explainable scoring function over a small reference table, matching
the spec's "rule-based/ML-ready architecture" requirement for §5.
A trained model can replace CROP_REFERENCE + score logic later
without changing predict()'s signature or PredictionResult shape,
so apps.crops and the frontend never need to change.
"""
from ml_models.common.predictor_base import BasePredictor, PredictionResult

# Reference ranges per crop. Values are illustrative agronomic
# midpoints/ranges commonly cited for Indian cropping conditions —
# NOT sourced from a specific dataset, and should be replaced with a
# vetted dataset or trained model before any real farming decision
# relies on them.
CROP_REFERENCE = [
    {
        "name": "Rice", "season": "Kharif",
        "n": (80, 120), "p": (30, 60), "k": (30, 60), "ph": (5.5, 7.0),
        "temperature": (20, 35), "humidity": (60, 90), "rainfall": (150, 300),
        "soil_types": {"alluvial", "clay", "loamy"},
        "water_requirement": "High", "duration_days": 120,
        "tips": "Requires standing water for most of the growth cycle; transplant seedlings after 20-25 days.",
    },
    {
        "name": "Cotton", "season": "Kharif",
        "n": (60, 100), "p": (30, 50), "k": (30, 60), "ph": (6.0, 8.0),
        "temperature": (21, 35), "humidity": (40, 70), "rainfall": (60, 120),
        "soil_types": {"black", "alluvial"},
        "water_requirement": "Medium", "duration_days": 180,
        "tips": "Black soil retains moisture well; avoid waterlogging during boll formation.",
    },
    {
        "name": "Maize", "season": "Kharif",
        "n": (100, 150), "p": (40, 60), "k": (40, 60), "ph": (5.5, 7.5),
        "temperature": (18, 32), "humidity": (50, 80), "rainfall": (50, 100),
        "soil_types": {"loamy", "alluvial", "red"},
        "water_requirement": "Medium", "duration_days": 100,
        "tips": "Sensitive to waterlogging; ensure good drainage.",
    },
    {
        "name": "Wheat", "season": "Rabi",
        "n": (100, 140), "p": (40, 60), "k": (30, 50), "ph": (6.0, 7.5),
        "temperature": (10, 25), "humidity": (40, 70), "rainfall": (30, 100),
        "soil_types": {"loamy", "alluvial", "clay"},
        "water_requirement": "Medium", "duration_days": 130,
        "tips": "Needs cool weather for germination and warm weather at maturity.",
    },
    {
        "name": "Groundnut", "season": "Kharif",
        "n": (20, 40), "p": (40, 60), "k": (40, 60), "ph": (6.0, 7.0),
        "temperature": (25, 35), "humidity": (50, 75), "rainfall": (50, 125),
        "soil_types": {"sandy", "red", "loamy"},
        "water_requirement": "Low", "duration_days": 110,
        "tips": "Prefers well-drained sandy loam; avoid heavy clay soils.",
    },
    {
        "name": "Chickpea (Bengal Gram)", "season": "Rabi",
        "n": (20, 40), "p": (40, 60), "k": (20, 40), "ph": (6.0, 7.5),
        "temperature": (10, 30), "humidity": (30, 60), "rainfall": (30, 65),
        "soil_types": {"black", "loamy", "clay"},
        "water_requirement": "Low", "duration_days": 100,
        "tips": "A drought-tolerant legume; avoid excess irrigation.",
    },
    {
        "name": "Sugarcane", "season": "Year-round (planted Feb-Mar or Oct)",
        "n": (150, 250), "p": (50, 80), "k": (80, 120), "ph": (6.0, 7.5),
        "temperature": (20, 38), "humidity": (60, 85), "rainfall": (100, 200),
        "soil_types": {"alluvial", "black", "loamy"},
        "water_requirement": "High", "duration_days": 365,
        "tips": "Long-duration, water-intensive crop; needs consistent irrigation.",
    },
]


def _range_score(value, low, high):
    """1.0 if inside range, decaying toward 0 the further outside it is."""
    if value is None:
        return 0.5  # neutral if the farmer didn't provide this input
    if low <= value <= high:
        return 1.0
    spread = max(high - low, 1)
    distance = (low - value) if value < low else (value - high)
    return max(0.0, 1.0 - distance / spread)


class CropRecommendationPredictor(BasePredictor):
    """
    Expected `inputs` keys (all optional except improving accuracy):
        soil_type, n, p, k, ph, temperature, humidity, rainfall,
        season, location, land_area, irrigation_available
    """

    def is_ready(self) -> bool:
        return True

    def predict(self, inputs: dict) -> list[PredictionResult]:
        soil_type = (inputs.get("soil_type") or "").lower()
        season = (inputs.get("season") or "").lower()

        results = []
        for crop in CROP_REFERENCE:
            scores = [
                _range_score(inputs.get("n"), *crop["n"]),
                _range_score(inputs.get("p"), *crop["p"]),
                _range_score(inputs.get("k"), *crop["k"]),
                _range_score(inputs.get("ph"), *crop["ph"]),
                _range_score(inputs.get("temperature"), *crop["temperature"]),
                _range_score(inputs.get("humidity"), *crop["humidity"]),
                _range_score(inputs.get("rainfall"), *crop["rainfall"]),
            ]
            numeric_score = sum(scores) / len(scores)

            soil_match = 1.0 if not soil_type or soil_type in crop["soil_types"] else 0.4
            season_match = 1.0 if not season or season in crop["season"].lower() else 0.6

            confidence = round(numeric_score * 0.7 + soil_match * 0.2 + season_match * 0.1, 3)

            results.append(
                PredictionResult(
                    label=crop["name"],
                    confidence=min(confidence, 0.98),  # never claim near-certainty from a rule table
                    details={
                        "expected_yield": "Varies by region and management practice",
                        "growing_duration_days": crop["duration_days"],
                        "water_requirement": crop["water_requirement"],
                        "soil_requirement": ", ".join(sorted(crop["soil_types"])),
                        "suitable_season": crop["season"],
                        "farming_tips": crop["tips"],
                    },
                    model_version="rule-based-v1",
                )
            )

        results.sort(key=lambda r: r.confidence, reverse=True)
        return results[:5]
