from django.conf import settings
from django.db import models

from apps.crops.models import Crop


class ProfitCalculation(models.Model):
    """
    Section 13: one saved run of the Smart Profit Calculator. Pure
    arithmetic (no ML/predictor involved) — computed and stored in
    the view, not derived from a predictor module.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profit_calculations"
    )
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True)
    land_area = models.DecimalField(max_digits=8, decimal_places=2)

    seed_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fertilizer_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    labour_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    irrigation_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pesticide_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    expected_yield = models.DecimalField(max_digits=10, decimal_places=2)  # in quintals
    expected_selling_price = models.DecimalField(max_digits=10, decimal_places=2)  # per quintal

    # Computed results, stored so history doesn't need to re-derive them
    total_investment = models.DecimalField(max_digits=12, decimal_places=2)
    expected_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    expected_profit = models.DecimalField(max_digits=12, decimal_places=2)
    cost_per_acre = models.DecimalField(max_digits=12, decimal_places=2)
    revenue_per_acre = models.DecimalField(max_digits=12, decimal_places=2)
    profit_margin_percent = models.DecimalField(max_digits=6, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Profit calc for {self.user} ({self.created_at:%Y-%m-%d})"
