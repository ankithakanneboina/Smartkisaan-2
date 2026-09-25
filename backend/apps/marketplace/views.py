from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.accounts.permissions import IsFarmerOrAdmin, IsBuyerOrAdmin, IsOwnerOrAdmin
from .models import Product, Wishlist
from .serializers import ProductSerializer

def _log_page_view(request, path):
    try:
        from apps.accounts.tracking_models import PageView
        PageView.objects.create(user=request.user if request.user.is_authenticated else None, path=path)
    except Exception:
        pass

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        qs = Product.objects.filter(is_available=True)
        if s := self.request.query_params.get("search"):
            qs = qs.filter(name__icontains=s) | qs.filter(description__icontains=s)
        if c := self.request.query_params.get("category"):
            qs = qs.filter(category=c)
        return qs.distinct()
    def get_serializer_context(self): return {"request": self.request}

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    def retrieve(self, request, *args, **kwargs):
        resp = super().retrieve(request, *args, **kwargs)
        _log_page_view(request, f"/api/marketplace/products/{kwargs.get('pk')}/")
        return resp
    def get_serializer_context(self): return {"request": self.request}

class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsFarmerOrAdmin]
    def perform_create(self, serializer):
        from apps.farmers.models import FarmerProfile
        profile = FarmerProfile.objects.filter(user=self.request.user).first()
        name = (profile.full_name if profile and profile.full_name else self.request.user.username)
        serializer.save(seller_name=name)
    def get_serializer_context(self): return {"request": self.request}

class ProductUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsFarmerOrAdmin, IsOwnerOrAdmin]
    queryset = Product.objects.all()
    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
    def get_serializer_context(self): return {"request": self.request}

class WishlistToggleView(APIView):
    permission_classes = [IsBuyerOrAdmin]
    def post(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if not product: return Response({"detail":"Not found."}, status=404)
        item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if not created: item.delete(); return Response({"is_wishlisted": False})
        return Response({"is_wishlisted": True})

class WishlistListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsBuyerOrAdmin]
    def get_queryset(self): return Product.objects.filter(wishlisted_by__user=self.request.user)
    def get_serializer_context(self): return {"request": self.request}

class FarmerOrdersView(APIView):
    permission_classes = [IsFarmerOrAdmin]
    def get(self, request):
        products = Product.objects.filter(seller_name__icontains=request.user.username)
        return Response({"detail":"Order management coming soon. Your listed products below.", "products": ProductSerializer(products, many=True, context={"request":request}).data})
