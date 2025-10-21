from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CarViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'cars', CarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
