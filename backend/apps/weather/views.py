from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.farmers.models import FarmerProfile
from .serializers import WeatherRecordSerializer
from .services.service import get_weather_for_location


class CurrentWeatherView(APIView):
    """
    GET /api/weather/current/?location=<name>
    Without a ?location= query param, falls back to the logged-in
    farmer's saved profile location. Powers the dashboard weather
    card in Phase 2.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        location = request.query_params.get("location")
        lat = lon = None

        if not location:
            profile = FarmerProfile.objects.filter(user=request.user).first()
            if profile and profile.location:
                location = profile.location
                lat, lon = profile.latitude, profile.longitude

        if not location:
            return Response(
                {"detail": "No location provided and no location saved in your profile."},
                status=400,
            )

        record = get_weather_for_location(location, latitude=lat, longitude=lon)
        return Response(WeatherRecordSerializer(record).data)
