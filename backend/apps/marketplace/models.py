from django.conf import settings
from django.db import models


class Product(models.Model):
    """
    Section 17: farmer marketplace listing. No payment processing per
    the spec's explicit instruction — `is_available` and `price` exist
    for display/filtering only. A real checkout flow (payment gateway,
    order model, transaction records) is a clean addition later behind
    this same Product model; nothing here needs to change for it.
    """

    class Category(models.TextChoices):
        SEEDS = "seeds", "Seeds"
        FERTILIZERS = "fertilizers", "Fertilizers"
        EQUIPMENT = "equipment", "Farming equipment"
        IRRIGATION_EQUIPMENT = "irrigation_equipment", "Irrigation equipment"
        ORGANIC_PRODUCTS = "organic_products", "Organic products"

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=Category.choices)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=30, default="unit")  # e.g. "per kg", "per unit"
    image_url = models.URLField(blank=True)

    seller_name = models.CharField(max_length=150)
    seller_contact = models.CharField(max_length=100, blank=True)

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    """One farmer's saved/wishlisted product."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
