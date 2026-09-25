from django.core.management.base import BaseCommand

from apps.diseases.models import Disease

# Demo reference data (§34) — general agronomic knowledge, not tied to
# any specific detection model's output classes yet.
DISEASE_SEED = [
    {
        "name": "Bacterial Leaf Blight",
        "crop_name": "Rice",
        "symptoms": "Water-soaked streaks on leaf margins turning yellow-to-white, wilting seedlings.",
        "possible_causes": "Xanthomonas oryzae bacteria, spread via water, wind-driven rain, contaminated tools.",
        "recommended_actions": "Drain field water, avoid excess nitrogen, remove and destroy infected plants.",
        "prevention_methods": "Use resistant varieties, treat seeds before sowing, avoid clipping leaf tips during transplanting.",
    },
    {
        "name": "Cotton Leaf Curl Virus",
        "crop_name": "Cotton",
        "symptoms": "Upward or downward curling of leaves, thickened veins, stunted growth.",
        "possible_causes": "Transmitted by whitefly (Bemisia tabaci); spreads rapidly in warm, dry conditions.",
        "recommended_actions": "Remove and destroy infected plants early, control whitefly population.",
        "prevention_methods": "Plant resistant varieties, avoid late sowing, monitor for whiteflies regularly.",
    },
    {
        "name": "Maize Leaf Blight",
        "crop_name": "Maize",
        "symptoms": "Long elliptical grey-green lesions on leaves, may merge and cause leaf death.",
        "possible_causes": "Fungal pathogen (Exserohilum turcicum), favored by humid, moderate-temperature conditions.",
        "recommended_actions": "Remove crop debris, rotate crops, apply approved fungicide if severe.",
        "prevention_methods": "Use resistant hybrids, avoid dense planting, ensure good field drainage.",
    },
    {
        "name": "Wheat Rust",
        "crop_name": "Wheat",
        "symptoms": "Orange-brown pustules on leaves and stems, reduced grain fill.",
        "possible_causes": "Fungal pathogen (Puccinia species), spreads via windborne spores.",
        "recommended_actions": "Apply approved fungicide at early signs, remove volunteer wheat plants nearby.",
        "prevention_methods": "Plant resistant varieties, timely sowing, avoid excess nitrogen application.",
    },
]


class Command(BaseCommand):
    help = "Seeds demo Disease reference catalog data (spec §34). Safe to re-run."

    def handle(self, *args, **options):
        created_count = 0
        for disease in DISEASE_SEED:
            _, created = Disease.objects.update_or_create(
                name=disease["name"], defaults=disease
            )
            created_count += created

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {created_count} new diseases (of {len(DISEASE_SEED)})."
        ))
