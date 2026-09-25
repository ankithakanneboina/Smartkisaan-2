from django.db import models

from apps.crops.models import Crop


class MarketPrice(models.Model):
    """
    Section 12: one price snapshot for a crop at a specific market/mandi
    on a specific date. Admin-managed/updateable, per spec (§15-style
    "keep data updateable from the admin panel" pattern extended here).
    Multiple rows per crop+market accumulate a price history, which the
    (labeled-as-estimate) trend endpoint reads from.
    """
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="market_prices")
    market_name = models.CharField(max_length=150)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default="per quintal")
    recorded_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-recorded_date"]
        indexes = [
            models.Index(fields=["crop", "recorded_date"]),
            models.Index(fields=["market_name"]),
        ]

    def __str__(self):
        return f"{self.crop.name} @ {self.market_name} ({self.recorded_date})"
