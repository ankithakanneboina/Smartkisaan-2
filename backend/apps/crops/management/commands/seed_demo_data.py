from django.core.management.base import BaseCommand

from ml_models.crop_recommendation.predictor import CROP_REFERENCE
from apps.crops.models import Crop
from apps.fertilizers.models import Fertilizer

# Demo data only (spec §34) — mirrors the fertilizer types the rule-based
# predictor recommends, so the catalog and the recommendation engine agree.
FERTILIZER_SEED = [
    {
        "name": "Urea",
        "fertilizer_type": "Nitrogen (N)",
        "application_method": "Broadcast and irrigate lightly, or split into basal + top-dressing doses.",
        "precautions": "Avoid application right before heavy rain — nitrogen leaches easily. Do not exceed recommended quantity.",
    },
    {
        "name": "DAP (Di-Ammonium Phosphate)",
        "fertilizer_type": "Phosphorus (P)",
        "application_method": "Apply as a basal dose at sowing/transplanting, placed near the root zone.",
        "precautions": "Do not mix directly with seed to avoid germination damage.",
    },
    {
        "name": "MOP (Muriate of Potash)",
        "fertilizer_type": "Potassium (K)",
        "application_method": "Apply as basal dose or split with top-dressing during fruiting/grain-fill stage.",
        "precautions": "Excess potash can affect calcium/magnesium uptake — follow recommended quantities.",
    },
]


class Command(BaseCommand):
    help = "Seeds demo Crop and Fertilizer catalog data (spec §34). Safe to re-run."

    def handle(self, *args, **options):
        crop_count = 0
        for crop in CROP_REFERENCE:
            _, created = Crop.objects.update_or_create(
                name=crop["name"],
                defaults={
                    "season": crop["season"],
                    "water_requirement": crop["water_requirement"],
                    "soil_requirement": ", ".join(sorted(crop["soil_types"])),
                    "growing_duration_days": crop["duration_days"],
                    "farming_tips": crop["tips"],
                },
            )
            crop_count += created

        fert_count = 0
        for fert in FERTILIZER_SEED:
            _, created = Fertilizer.objects.update_or_create(
                name=fert["name"], defaults=fert
            )
            fert_count += created

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {crop_count} new crops (of {len(CROP_REFERENCE)}), "
                f"{fert_count} new fertilizers (of {len(FERTILIZER_SEED)}). Existing rows updated in place."
            )
        )
