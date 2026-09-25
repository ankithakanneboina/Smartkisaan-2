"""
Rule-based fertilizer recommendation.

Compares the farmer's reported soil N/P/K against a target range for
the given crop (falls back to generic targets if the crop isn't in
CROP_TARGETS) and recommends fertilizers to close the biggest gaps.
Same "transparent now, swappable for a trained model later" pattern
as crop_recommendation/predictor.py — see that file's docstring.

IMPORTANT: this never recommends specific pesticide/chemical dosages
without a precaution note, per spec §9/§6 safety requirements.
"""
from ml_models.common.predictor_base import BasePredictor, PredictionResult

# Target NPK midpoints per crop (kg/ha) — illustrative, not a vetted
# agronomic dataset. Falls back to GENERIC_TARGET when crop is unknown.
CROP_TARGETS = {
    "rice": {"n": 100, "p": 45, "k": 45},
    "cotton": {"n": 80, "p": 40, "k": 45},
    "maize": {"n": 125, "p": 50, "k": 50},
    "wheat": {"n": 120, "p": 50, "k": 40},
    "groundnut": {"n": 30, "p": 50, "k": 50},
    "chickpea": {"n": 30, "p": 50, "k": 30},
    "sugarcane": {"n": 200, "p": 65, "k": 100},
}
GENERIC_TARGET = {"n": 100, "p": 50, "k": 50}

FERTILIZER_FOR_NUTRIENT = {
    "n": {"name": "Urea", "type": "Nitrogen (N)"},
    "p": {"name": "DAP (Di-Ammonium Phosphate)", "type": "Phosphorus (P)"},
    "k": {"name": "MOP (Muriate of Potash)", "type": "Potassium (K)"},
}

APPLICATION_STAGE_BY_STAGE = {
    "seedling": "Basal dose at sowing/transplanting",
    "vegetative": "Top-dressing during active vegetative growth",
    "flowering": "Split dose before flowering, avoid excess nitrogen",
    "fruiting": "Potassium-focused top-dressing to support fruit/grain fill",
    "": "Split into basal + top-dressing doses per crop stage",
}


class FertilizerRecommendationPredictor(BasePredictor):
    """
    Expected `inputs` keys:
        crop, soil_type, n, p, k, ph, growth_stage, land_area
    """

    def is_ready(self) -> bool:
        return True

    def predict(self, inputs: dict) -> list[PredictionResult]:
        crop = (inputs.get("crop") or "").strip().lower()
        target = CROP_TARGETS.get(crop, GENERIC_TARGET)
        growth_stage = (inputs.get("growth_stage") or "").strip().lower()
        land_area = float(inputs.get("land_area") or 1)

        current = {
            "n": inputs.get("n"),
            "p": inputs.get("p"),
            "k": inputs.get("k"),
        }

        results = []
        for nutrient, target_value in target.items():
            current_value = current.get(nutrient)
            deficit = target_value - current_value if current_value is not None else target_value * 0.5

            if deficit <= 0:
                continue  # nutrient already sufficient — no fertilizer needed for it

            # Rough kg-of-fertilizer-per-kg-of-nutrient conversion factors
            # (Urea ~46% N, DAP ~46% P2O5, MOP ~60% K2O) — approximate.
            conversion = {"n": 1 / 0.46, "p": 1 / 0.46, "k": 1 / 0.60}[nutrient]
            estimated_quantity_kg = round(deficit * conversion * land_area, 1)

            fert = FERTILIZER_FOR_NUTRIENT[nutrient]
            confidence = 0.9 if current_value is not None else 0.5  # lower confidence if guessing

            results.append(
                PredictionResult(
                    label=fert["name"],
                    confidence=confidence,
                    details={
                        "fertilizer_type": fert["type"],
                        "estimated_quantity_kg": estimated_quantity_kg,
                        "application_stage": APPLICATION_STAGE_BY_STAGE.get(
                            growth_stage, APPLICATION_STAGE_BY_STAGE[""]
                        ),
                        "application_method": "Broadcast evenly and irrigate lightly after application.",
                        "precautions": (
                            "Do not exceed the recommended quantity — over-application can damage "
                            "crops and soil health. If unsure, consult your local agriculture extension "
                            "officer before applying."
                        ),
                    },
                    model_version="rule-based-v1",
                )
            )

        results.sort(key=lambda r: r.confidence, reverse=True)
        return results
