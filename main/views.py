from rest_framework import viewsets, filters
from .models import User, Car
from .serializers import UserSerializer, CarSerializer
from django_filters.rest_framework import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user_firstname', 'user_lastname']
    search_fields = ['user_firstname', 'user_lastname', 'cars__car_model']

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['car_brand', 'car_color']
    search_fields = ['car_brand', 'car_model', 'owners__user_firstname']
