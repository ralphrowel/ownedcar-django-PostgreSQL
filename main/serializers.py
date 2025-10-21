from rest_framework import serializers
from .models import User, Car, CarOwnership

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class CarOwnershipSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)

    class Meta:
        model = CarOwnership
        fields = ['id', 'car', 'ownership_type', 'date_acquired']


class UserSerializer(serializers.ModelSerializer):
    owned_cars = CarOwnershipSerializer(source='carownership_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'user_firstname', 'user_lastname', 'owned_cars']
