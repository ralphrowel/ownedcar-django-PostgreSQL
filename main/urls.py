from rest_framework import routers
from .views import UserViewSet, CarViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'cars', CarViewSet)

urlpatterns = router.urls
