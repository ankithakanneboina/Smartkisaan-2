from rest_framework import serializers

from .models import GovernmentScheme


class GovernmentSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentScheme
        fields = (
            "id", "name", "category", "description", "eligibility",
            "benefits", "required_documents", "application_process",
            "official_link", "updated_at",
        )
