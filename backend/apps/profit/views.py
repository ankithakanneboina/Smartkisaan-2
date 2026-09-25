from decimal import Decimal, ROUND_HALF_UP

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.crops.models import Crop
from .models import ProfitCalculation
from .serializers import ProfitCalculationRequestSerializer, ProfitCalculationSerializer


def _round2(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class ProfitCalculateView(APIView):
    """
    POST /api/profit/calculate/
    Pure arithmetic per §13 — no predictor involved. Saves the run so
    it shows up in /api/profit/history/ and (later) the profit
    comparison feature.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        input_serializer = ProfitCalculationRequestSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        v = input_serializer.validated_data

        total_investment = (
            v["seed_cost"] + v["fertilizer_cost"] + v["labour_cost"]
            + v["irrigation_cost"] + v["pesticide_cost"] + v["other_expenses"]
        )
        expected_revenue = v["expected_yield"] * v["expected_selling_price"]
        expected_profit = expected_revenue - total_investment

        land_area = v["land_area"] or Decimal("1")
        cost_per_acre = total_investment / land_area if land_area else Decimal("0")
        revenue_per_acre = expected_revenue / land_area if land_area else Decimal("0")
        profit_margin_percent = (
            (expected_profit / expected_revenue * 100) if expected_revenue else Decimal("0")
        )

        crop_obj = None
        crop_name = v.get("crop", "")
        if crop_name:
            crop_obj = Crop.objects.filter(name__iexact=crop_name).first()

        record = ProfitCalculation.objects.create(
            user=request.user,
            crop=crop_obj,
            land_area=v["land_area"],
            seed_cost=v["seed_cost"],
            fertilizer_cost=v["fertilizer_cost"],
            labour_cost=v["labour_cost"],
            irrigation_cost=v["irrigation_cost"],
            pesticide_cost=v["pesticide_cost"],
            other_expenses=v["other_expenses"],
            expected_yield=v["expected_yield"],
            expected_selling_price=v["expected_selling_price"],
            total_investment=_round2(total_investment),
            expected_revenue=_round2(expected_revenue),
            expected_profit=_round2(expected_profit),
            cost_per_acre=_round2(cost_per_acre),
            revenue_per_acre=_round2(revenue_per_acre),
            profit_margin_percent=_round2(profit_margin_percent),
        )
        return Response(ProfitCalculationSerializer(record).data)


class ProfitCalculationHistoryView(generics.ListAPIView):
    """GET /api/profit/history/ — the logged-in farmer's past calculations."""
    serializer_class = ProfitCalculationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProfitCalculation.objects.filter(user=self.request.user)
