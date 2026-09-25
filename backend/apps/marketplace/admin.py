from django.contrib import admin

from .models import Product, Wishlist


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "unit", "seller_name", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description", "seller_name")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")
