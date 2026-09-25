from rest_framework import generics, permissions

from .models import GovernmentScheme
from .serializers import GovernmentSchemeSerializer


class GovernmentSchemeListView(generics.ListAPIView):
    """
    GET /api/schemes/?search=&category=
    §15: search + category filter. Content is entirely admin-managed
    (see models.py) — this view never generates scheme text.
    """
    serializer_class = GovernmentSchemeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = GovernmentScheme.objects.all()

        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(name__icontains=search) | qs.filter(description__icontains=search)

        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category__iexact=category)

        return qs.distinct()


class GovernmentSchemeDetailView(generics.RetrieveAPIView):
    """GET /api/schemes/<id>/"""
    queryset = GovernmentScheme.objects.all()
    serializer_class = GovernmentSchemeSerializer
    permission_classes = [permissions.IsAuthenticated]
