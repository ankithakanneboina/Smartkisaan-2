import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.crops.models import Crop
from apps.market.models import MarketPrice

# Illustrative demo prices only (spec §34) — NOT sourced from any real
# mandi data feed. A real deployment should replace this with an actual
# market-data integration (e.g. Agmarknet) before farmers rely on it.
MARKET_SEED = {
    "Rice": {"base": 2100, "markets": ["Warangal Mandi", "Karimnagar Mandi"]},
    "Cotton": {"base": 7200, "markets": ["Adilabad Mandi", "Guntur Mandi"]},
    "Maize": {"base": 1900, "markets": ["Nizamabad Mandi"]},
    "Wheat": {"base": 2300, "markets": ["Karimnagar Mandi"]},
    "Groundnut": {"base": 5800, "markets": ["Anantapur Mandi"]},
    "Chickpea (Bengal Gram)": {"base": 5200, "markets": ["Kurnool Mandi"]},
    "Sugarcane": {"base": 320, "markets": ["Nizamabad Mandi"]},
}


class Command(BaseCommand):
    help = "Seeds 14 days of demo MarketPrice history per crop (spec §34). Safe to re-run."

    def handle(self, *args, **options):
        created_count = 0
        today = timezone.now().date()

        for crop_name, info in MARKET_SEED.items():
            crop = Crop.objects.filter(name=crop_name).first()
            if not crop:
                self.stdout.write(self.style.WARNING(
                    f"Skipping {crop_name} — run seed_demo_data (crops) first."
                ))
                continue

            for market_name in info["markets"]:
                rng = random.Random(f"{crop_name}-{market_name}")
                base = info["base"]
                for days_ago in range(14, -1, -1):
                    day = today - timedelta(days=days_ago)
                    drift = rng.uniform(-0.04, 0.04) * base
                    current = round(base + drift, 2)
                    _, created = MarketPrice.objects.update_or_create(
                        crop=crop, market_name=market_name, recorded_date=day,
                        defaults={
                            "current_price": current,
                            "min_price": round(current * 0.95, 2),
                            "max_price": round(current * 1.05, 2),
                            "unit": "per quintal",
                        },
                    )
                    created_count += created

        self.stdout.write(self.style.SUCCESS(f"Seeded {created_count} new market price rows."))
