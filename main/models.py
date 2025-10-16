from django.db import models

class User(models.Model):
    user_firstname = models.CharField(max_length=200)
    user_lastname = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user_firstname} {self.user_lastname}"

class Car(models.Model):
    COLORS = [
        ("black", "Black"),
        ("silver", "Silver"),
        ("white", "White"),
        ("bronze", "Bronze"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cars",
        null=True,
        blank=True,
        help_text="The primary owner of this car.",
    )
    car_brand = models.CharField(max_length=200, default="unknown")
    car_model = models.CharField(max_length=200)
    car_color = models.CharField(max_length=20, choices=COLORS, default="black")
    car_platenumber = models.IntegerField(unique=True, null=True, blank=True, default=0)

    shared_with = models.ManyToManyField(
        User,
        related_name="shared_cars",
        blank=True,
        help_text="Users this car is shared with.",
    )

    def __str__(self):
        return f"{self.car_brand} {self.car_model} ({self.car_color})"

class PurchaseInfo(models.Model):
    car = models.OneToOneField(
        Car,
        on_delete=models.CASCADE,
        related_name="purchase_info",
        help_text="The car associated with this purchase record.",
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="purchased_cars",
        help_text="The user who bought the car.",
    )
    purchase_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Purchase of {self.car} by {self.buyer} on {self.purchase_date}"

class BorrowedCar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    borrowed_from = models.DateField()
    borrowed_until = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} borrowed {self.car} from {self.borrowed_from} to {self.borrowed_until or 'Present'}"


Car.add_to_class(
    'borrowers',
    models.ManyToManyField(
        User,
        through='BorrowedCar',
        related_name='borrowed_cars',
        blank=True,
        help_text="Users who have borrowed this car.",
    )
)
