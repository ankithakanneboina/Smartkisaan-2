from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# Each app owns its own /api/<app>/ namespace — new apps in later
# phases just add one more include() line here.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/admin/", include("apps.accounts.admin_urls")),
    path("api/farmers/", include("apps.farmers.urls")),
    path("api/weather/", include("apps.weather.urls")),
    path("api/farm-activities/", include("apps.activities.urls")),
    path("api/reminders/", include("apps.reminders.urls")),
    path("api/crops/", include("apps.crops.urls")),
    path("api/fertilizers/", include("apps.fertilizers.urls")),
    path("api/market/", include("apps.market.urls")),
    path("api/profit/", include("apps.profit.urls")),
    path("api/diseases/", include("apps.diseases.urls")),
    path("api/ai/", include("apps.ai_assistant.urls")),
    path("api/farm-plan/", include("apps.farm_plan.urls")),
    path("api/schemes/", include("apps.schemes.urls")),
    path("api/videos/", include("apps.videos.urls")),
    path("api/marketplace/", include("apps.marketplace.urls")),
    path("api/community/", include("apps.community.urls")),
    path("api/analytics/", include("apps.analytics.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
