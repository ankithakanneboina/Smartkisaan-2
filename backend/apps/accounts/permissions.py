from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    message = "Admin access required."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin_role)

class IsFarmer(BasePermission):
    message = "Farmer account required."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_farmer)

class IsBuyer(BasePermission):
    message = "Buyer account required."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_buyer)

class IsFarmerOrAdmin(BasePermission):
    message = "Farmer or admin access required."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_farmer or request.user.is_admin_role))

class IsBuyerOrAdmin(BasePermission):
    message = "Buyer or admin access required."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_buyer or request.user.is_admin_role))

class IsOwnerOrAdmin(BasePermission):
    message = "You can only access your own resources."
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin_role:
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "owner", None)
        return owner == request.user
