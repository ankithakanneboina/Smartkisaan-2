from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import FarmerProfile
from .serializers import FarmerProfileSerializer


class MyFarmerProfileView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT/PATCH /api/farmers/me/
    Creates an empty profile on first GET so the frontend can always
    render an editable form right after registration, per section 3
    ("Farmer profile should optionally contain ...").
    Accepts multipart form data so profile_photo can be uploaded in
    the same PATCH as the other fields.
    """
    serializer_class = FarmerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        profile, _ = FarmerProfile.objects.get_or_create(user=self.request.user)
        return profile
