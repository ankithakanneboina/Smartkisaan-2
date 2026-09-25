from rest_framework import serializers
from .models import Product, Wishlist

class ProductSerializer(serializers.ModelSerializer):
    is_wishlisted = serializers.SerializerMethodField()
    seller_name = serializers.CharField(required=False, default="")

    class Meta:
        model = Product
        fields = ("id","name","category","description","price","unit","image_url","seller_name","seller_contact","is_available","is_wishlisted","created_at")

    def get_is_wishlisted(self, obj):
        user = self.context.get("request").user if self.context.get("request") else None
        if not user or not user.is_authenticated: return False
        return Wishlist.objects.filter(user=user, product=obj).exists()
