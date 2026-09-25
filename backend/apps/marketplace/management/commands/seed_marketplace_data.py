from django.core.management.base import BaseCommand

from apps.marketplace.models import Product

# Demo listings only (§34), clearly fictional sellers/prices —
# replace via /admin/ with real listings before production use.
PRODUCT_SEED = [
    {
        "name": "Hybrid Cotton Seeds (1kg pack)",
        "category": "seeds",
        "description": "High-yield hybrid cotton seed variety, demo listing.",
        "price": 850, "unit": "per kg pack",
        "seller_name": "Demo Seed Supplier Co.",
    },
    {
        "name": "Urea Fertilizer (50kg bag)",
        "category": "fertilizers",
        "description": "Standard nitrogen fertilizer, demo listing.",
        "price": 350, "unit": "per 50kg bag",
        "seller_name": "Demo Agro Supplies",
    },
    {
        "name": "Manual Seed Drill",
        "category": "equipment",
        "description": "Hand-operated seed drill for small plots, demo listing.",
        "price": 4500, "unit": "per unit",
        "seller_name": "Demo Farm Equipment Store",
    },
    {
        "name": "Drip Irrigation Kit (1 acre)",
        "category": "irrigation_equipment",
        "description": "Basic drip irrigation setup for one acre, demo listing.",
        "price": 12000, "unit": "per kit",
        "seller_name": "Demo Irrigation Solutions",
    },
    {
        "name": "Vermicompost (25kg bag)",
        "category": "organic_products",
        "description": "Organic vermicompost fertilizer, demo listing.",
        "price": 400, "unit": "per 25kg bag",
        "seller_name": "Demo Organic Farms",
    },
]


class Command(BaseCommand):
    help = "Seeds demo marketplace products with fictional prices/sellers (spec §34). Safe to re-run."

    def handle(self, *args, **options):
        created_count = 0
        for product in PRODUCT_SEED:
            _, created = Product.objects.update_or_create(
                name=product["name"], defaults=product
            )
            created_count += created

        self.stdout.write(self.style.WARNING(
            f"Seeded {created_count} new demo products — fictional sellers/prices, "
            "replace via /admin/ before production use."
        ))
