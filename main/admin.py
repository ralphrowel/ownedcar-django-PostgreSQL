from django.contrib import admin
from .models import User, Car, CarOwnership, PurchaseInfo


class CarOwnershipInline(admin.TabularInline):
    """Inline display of car ownership details inside Car or User admin."""
    model = CarOwnership
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_firstname', 'user_lastname', 'get_owned_cars', 'get_shared_cars')
    search_fields = ('user_firstname', 'user_lastname', 'owned_cars__car_brand', 'owned_cars__car_model')
    inlines = [CarOwnershipInline]

    def get_owned_cars(self, obj):
        owned = obj.owned_cars.filter(carownership__ownership_type="owner")
        return ", ".join([f"{c.car_brand} {c.car_model}" for c in owned]) if owned else "-"
    get_owned_cars.short_description = "Owned Cars"

    def get_shared_cars(self, obj):
        shared = obj.owned_cars.filter(carownership__ownership_type="shared")
        return ", ".join([f"{c.car_brand} {c.car_model}" for c in shared]) if shared else "-"
    get_shared_cars.short_description = "Shared Cars"


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_brand', 'car_model', 'car_color', 'car_platenumber', 'get_owners')
    search_fields = ('car_brand', 'car_model', 'car_platenumber', 'owners__user_firstname', 'owners__user_lastname')
    list_filter = ('car_color',)
    inlines = [CarOwnershipInline]

    def get_owners(self, obj):
        owners = obj.owners.filter(carownership__ownership_type="owner")
        return ", ".join([f"{u.user_firstname} {u.user_lastname}" for u in owners]) if owners else "-"
    get_owners.short_description = "Owners"


@admin.register(CarOwnership)
class CarOwnershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'ownership_type', 'date_acquired')
    list_filter = ('ownership_type', 'date_acquired')
    search_fields = ('user__user_firstname', 'user__user_lastname', 'car__car_brand', 'car__car_model')


@admin.register(PurchaseInfo)
class PurchaseInfoAdmin(admin.ModelAdmin):
    list_display = ('car', 'buyer', 'purchase_date', 'price')
    list_filter = ('purchase_date',)
    search_fields = ('car__car_brand', 'car__car_model', 'buyer__user_firstname', 'buyer__user_lastname')
