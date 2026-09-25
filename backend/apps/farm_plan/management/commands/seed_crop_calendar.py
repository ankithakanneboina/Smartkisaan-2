from django.core.management.base import BaseCommand

from apps.crops.models import Crop
from apps.farm_plan.models import CropCalendarStage

# Demo lifecycle templates (§34) — illustrative week ranges, not a
# vetted agronomic source. Land prep/sowing/germination/fertilizer/
# irrigation/disease-monitoring/harvest per §14, scaled loosely to
# each crop's known growing_duration_days.
STAGE_TEMPLATE = [
    ("Land preparation", "Plough and level the field; incorporate organic matter.", 0, 1),
    ("Sowing", "Sow seeds/transplant seedlings at recommended spacing.", 1, 1),
    ("Germination", "Monitor for even germination; irrigate lightly and consistently.", 1, 3),
    ("Fertilizer stage (basal + early top-dressing)", "Apply basal fertilizer dose; first top-dressing as growth begins.", 3, 5),
    ("Irrigation stage (vegetative growth)", "Maintain consistent soil moisture through active vegetative growth.", 4, 10),
    ("Disease/pest monitoring", "Inspect regularly for early signs of pests or disease; treat promptly if found.", 5, 12),
    ("Harvest", "Harvest when the crop reaches maturity indicators for this variety.", 0, 0),  # placeholder, overridden below
]


class Command(BaseCommand):
    help = "Seeds CropCalendarStage rows for all crops in the catalog (spec §14/§34). Safe to re-run."

    def handle(self, *args, **options):
        created_count = 0
        for crop in Crop.objects.all():
            duration_weeks = max((crop.growing_duration_days or 90) // 7, 4)
            harvest_week = duration_weeks

            stages = list(STAGE_TEMPLATE)
            stages[-1] = (stages[-1][0], stages[-1][1], harvest_week, harvest_week + 1)

            for order, (name, desc, week_start, week_end) in enumerate(stages, start=1):
                _, created = CropCalendarStage.objects.update_or_create(
                    crop=crop, stage_order=order,
                    defaults={
                        "stage_name": name,
                        "description": desc,
                        "typical_week_start": max(week_start, 1),
                        "typical_week_end": max(week_end, week_start + 1),
                    },
                )
                created_count += created

        self.stdout.write(self.style.SUCCESS(f"Seeded {created_count} new crop calendar stage rows."))
