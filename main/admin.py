from django.contrib import admin
from .models import User, Car, CarOwnership, PurchaseInfo


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_firstname', 'user_lastname', 'role', 'owned_cars_list', 'shared_cars_list')
    list_filter = ('role',)
    search_fields = ('user_firstname', 'user_lastname', 'role')

    def owned_cars_list(self, obj):
        cars = obj.owned_cars.all()
        return ", ".join([f"{c.car_brand} {c.car_model}" for c in cars]) if cars else "-"
    owned_cars_list.short_description = "Owned Cars"

    def shared_cars_list(self, obj):
        cars = CarOwnership.objects.filter(user=obj, ownership_type="shared").select_related("car")
        return ", ".join([f"{co.car.car_brand} {co.car.car_model}" for co in cars]) if cars else "-"
    shared_cars_list.short_description = "Shared Cars"


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_brand', 'car_model', 'car_color', 'car_platenumber', 'get_owners')
    search_fields = ('car_brand', 'car_model', 'car_platenumber', 'owners__user_firstname', 'owners__user_lastname')
    list_filter = ('car_color',)

    def get_owners(self, obj):
        users = obj.owners.all()
        return ", ".join([f"{u.user_firstname} {u.user_lastname}" for u in users]) if users else "-"
    get_owners.short_description = "Owners"


@admin.register(CarOwnership)
class CarOwnershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'ownership_type', 'date_acquired')
    list_filter = ('ownership_type',)


@admin.register(PurchaseInfo)
class PurchaseInfoAdmin(admin.ModelAdmin):
    list_display = ('car', 'buyer', 'purchase_date', 'price')
