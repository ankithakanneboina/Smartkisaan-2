from django.core.management.base import BaseCommand

from apps.videos.models import Video

# Demo library structure only (§34) — deliberately using placeholder
# URLs rather than inventing real YouTube links, since Claude can't
# verify a specific video actually exists/is accurate. Replace these
# via /admin/ with real, vetted videos before using this in production.
VIDEO_SEED = [
    {
        "title": "Getting Started with Organic Farming",
        "category": "organic_farming",
        "description": "Placeholder entry — replace with a real, vetted video via /admin/.",
        "video_url": "https://example.com/videos/organic-farming-intro",
    },
    {
        "title": "Drip Irrigation Setup Basics",
        "category": "irrigation",
        "description": "Placeholder entry — replace with a real, vetted video via /admin/.",
        "video_url": "https://example.com/videos/drip-irrigation-basics",
    },
    {
        "title": "Identifying Common Pests in Cotton",
        "category": "pest_management",
        "description": "Placeholder entry — replace with a real, vetted video via /admin/.",
        "video_url": "https://example.com/videos/cotton-pest-identification",
    },
    {
        "title": "Soil Testing at Home — A Simple Guide",
        "category": "soil_management",
        "description": "Placeholder entry — replace with a real, vetted video via /admin/.",
        "video_url": "https://example.com/videos/home-soil-testing",
    },
    {
        "title": "Understanding NPK Fertilizers",
        "category": "fertilizers",
        "description": "Placeholder entry — replace with a real, vetted video via /admin/.",
        "video_url": "https://example.com/videos/npk-fertilizers-explained",
    },
]


class Command(BaseCommand):
    help = (
        "Seeds demo video library structure with PLACEHOLDER urls (spec §34). "
        "Safe to re-run. Replace video_url values via /admin/ with real content before production use."
    )

    def handle(self, *args, **options):
        created_count = 0
        for video in VIDEO_SEED:
            _, created = Video.objects.update_or_create(
                title=video["title"], defaults=video
            )
            created_count += created

        self.stdout.write(self.style.WARNING(
            f"Seeded {created_count} new videos with PLACEHOLDER URLs — "
            "replace via /admin/ before production use."
        ))
