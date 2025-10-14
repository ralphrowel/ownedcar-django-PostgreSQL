from django.contrib import admin
from .models import User, Car

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_firstname', 'user_lastname', 'get_car_brand', 'get_car_model', 'get_car_color', 'get_car_platenumber')
    search_fields = ('user_firstname', 'user_lastname', 'car__car_model', 'car__car_brand')

    def get_car_brand(self, obj):
        return obj.car.car_brand if obj.car else '-'
    get_car_brand.short_description = 'Car Brand'

    def get_car_model(self, obj):
        return obj.car.car_model if obj.car else '-'
    get_car_model.short_description = 'Car Model'

    def get_car_color(self, obj):
        return obj.car.car_color if obj.car else '-'
    get_car_color.short_description = 'Car Color'

    def get_car_platenumber(self, obj):
        return obj.car.car_platenumber if obj.car else '-'
    get_car_platenumber.short_description = 'Plate Number'


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_brand', 'car_model', 'car_color', 'car_platenumber')
    search_fields = ('car_brand', 'car_model', 'car_platenumber')
