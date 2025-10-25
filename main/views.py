from rest_framework import permissions, viewsets
from .models import Car, User
from .serializers import CarSerializer, UserSerializer


# ---- PERMISSIONS ----
class IsDealerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role in ["dealer", "admin"]
        )


# ---- USER VIEWSET ----
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # anyone can view users for now


# ---- CAR VIEWSET ----
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsDealerOrAdmin()]
        return [permissions.AllowAny()]
