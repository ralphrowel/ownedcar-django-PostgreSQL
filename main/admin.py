from django.contrib import admin
from .models import User, Car, PurchaseInfo, BorrowedCar

class PurchaseInfoInline(admin.StackedInline):
    """Inline to show or edit purchase info directly inside a car entry."""
    model = PurchaseInfo
    extra = 0
    can_delete = False


class BorrowedCarInline(admin.TabularInline):
    """Inline to manage users who borrowed this car."""
    model = BorrowedCar
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_firstname',
        'user_lastname',
        'owned_cars_list',
        'shared_cars_list',
        'borrowed_cars_list',
    )
    search_fields = (
        'user_firstname',
        'user_lastname',
        'cars__car_brand',
        'cars__car_model',
    )

    def owned_cars_list(self, obj):
        """Show all cars owned by the user."""
        cars = obj.cars.all()
        return ", ".join([f"{c.car_brand} {c.car_model}" for c in cars]) if cars else "-"
    owned_cars_list.short_description = "Owned Cars"

    def shared_cars_list(self, obj):
        """Show all cars shared with the user."""
        cars = obj.shared_cars.all()
        return ", ".join([f"{c.car_brand} {c.car_model}" for c in cars]) if cars else "-"
    shared_cars_list.short_description = "Shared Cars"

    def borrowed_cars_list(self, obj):
        """Show all cars the user has borrowed."""
        cars = obj.borrowed_cars.all()
        return ", ".join([f"{c.car_brand} {c.car_model}" for c in cars]) if cars else "-"
    borrowed_cars_list.short_description = "Borrowed Cars"

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'car_brand',
        'car_model',
        'car_color',
        'car_platenumber',
        'owner',
        'get_shared_users',
    )
    search_fields = (
        'car_brand',
        'car_model',
        'car_platenumber',
        'owner__user_firstname',
        'owner__user_lastname',
    )
    list_filter = ('car_color',)
    inlines = [PurchaseInfoInline, BorrowedCarInline]
    filter_horizontal = ('shared_with',)

    def get_shared_users(self, obj):
        """Show users this car is shared with."""
        users = obj.shared_with.all()
        return ", ".join([f"{u.user_firstname} {u.user_lastname}" for u in users]) if users else "-"
    get_shared_users.short_description = "Shared With"

@admin.register(BorrowedCar)
class BorrowedCarAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'borrowed_from', 'borrowed_until')
    list_filter = ('borrowed_from', 'borrowed_until')
    search_fields = (
        'user__user_firstname',
        'user__user_lastname',
        'car__car_brand',
        'car__car_model',
    )

@admin.register(PurchaseInfo)
class PurchaseInfoAdmin(admin.ModelAdmin):
    list_display = ('car', 'buyer', 'purchase_date', 'price')
    search_fields = (
        'car__car_brand',
        'car__car_model',
        'buyer__user_firstname',
        'buyer__user_lastname',
    )
    list_filter = ('purchase_date',)
