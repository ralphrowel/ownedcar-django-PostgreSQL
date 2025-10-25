from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Car, CarOwnership
from .serializers import UserSerializer, CarSerializer, CarOwnershipSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user_firstname', 'user_lastname']
    search_fields = ['user_firstname', 'user_lastname', 'carownership__car__car_model']

    @action(detail=True, methods=['get', 'post'])
    def cars(self, request, pk=None):
        user = self.get_object()

        if request.method == 'GET':
            ownerships = CarOwnership.objects.filter(user=user)
            serializer = CarOwnershipSerializer(ownerships, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            car_id = request.data.get('car_id')
            ownership_type = request.data.get('ownership_type', 'owner')
            car = Car.objects.get(id=car_id)
            ownership, created = CarOwnership.objects.get_or_create(
                user=user, car=car, defaults={'ownership_type': ownership_type}
            )
            if not created:
                ownership.ownership_type = ownership_type
                ownership.save()
            return Response(CarOwnershipSerializer(ownership).data)


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['car_brand', 'car_color']
    search_fields = ['car_brand', 'car_model', 'owners__user_firstname']

    @action(detail=True, methods=['get'])
    def owners(self, request, pk=None):
        car = self.get_object()
        ownerships = CarOwnership.objects.filter(car=car)
        serializer = CarOwnershipSerializer(ownerships, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny]