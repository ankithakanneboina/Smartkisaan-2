from django.db.models import Max
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MarketPrice
from .serializers import MarketPriceSerializer, MarketTrendPointSerializer

SORT_FIELDS = {
    "price_asc": "current_price",
    "price_desc": "-current_price",
    "date_asc": "recorded_date",
    "date_desc": "-recorded_date",
}


class MarketPriceListView(generics.ListAPIView):
    """
    GET /api/market/prices/?crop=<name>&market=<name>&sort=<key>
    Manual query filtering (no extra dependency) — §12's search/filter/sort.
    Only the latest snapshot per crop+market is returned so the list
    doesn't show duplicate stale rows; full history is on /trend/.
    """
    serializer_class = MarketPriceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = MarketPrice.objects.select_related("crop")

        crop = self.request.query_params.get("crop")
        if crop:
            qs = qs.filter(crop__name__icontains=crop)

        market = self.request.query_params.get("market")
        if market:
            qs = qs.filter(market_name__icontains=market)

        # Keep only each crop+market's most recent row (avoids showing
        # 15 stale duplicate rows per pair from the seeded history).
        latest_dates = (
            qs.values("crop_id", "market_name")
            .annotate(latest=Max("recorded_date"))
        )
        latest_pairs = {(row["crop_id"], row["market_name"], row["latest"]) for row in latest_dates}
        ids = [
            row.id for row in qs
            if (row.crop_id, row.market_name, row.recorded_date) in latest_pairs
        ]
        qs = qs.filter(id__in=ids)

        sort_key = self.request.query_params.get("sort")
        if sort_key in SORT_FIELDS:
            qs = qs.order_by(SORT_FIELDS[sort_key])

        return qs


class MarketPriceTrendView(APIView):
    """
    GET /api/market/prices/trend/?crop=<name>&market=<name>
    Returns the crop's price history as a simple date/price series.
    This is historical data, not a forecast — the response is
    explicitly labeled so the frontend never presents it as a
    prediction (§12: "Clearly label predictions as estimates").
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        crop = request.query_params.get("crop")
        market = request.query_params.get("market")
        if not crop:
            return Response({"detail": "?crop=<name> is required."}, status=400)

        qs = MarketPrice.objects.filter(crop__name__icontains=crop)
        if market:
            qs = qs.filter(market_name__icontains=market)
        qs = qs.order_by("recorded_date")

        points = [{"date": row.recorded_date, "price": row.current_price} for row in qs]
        serialized = MarketTrendPointSerializer(points, many=True).data

        return Response({
            "crop": crop,
            "market": market or "all markets",
            "history": serialized,
            "label": "historical_data_not_a_prediction",
        })
