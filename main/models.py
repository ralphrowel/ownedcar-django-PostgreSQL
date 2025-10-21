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

    car_brand = models.CharField(max_length=200, default="unknown")
    car_model = models.CharField(max_length=200)
    car_color = models.CharField(max_length=20, choices=COLORS, default="black")
    car_platenumber = models.IntegerField(unique=True, null=True, blank=True, default=0)

    # A car can have multiple owners (shared), and each ownership has details
    owners = models.ManyToManyField(
        User,
        through='CarOwnership',
        related_name='owned_cars',
        blank=True,
        help_text="Users who own or share this car.",
    )

    def __str__(self):
        return f"{self.car_brand} {self.car_model} ({self.car_color})"


class CarOwnership(models.Model):
    OWNERSHIP_TYPE = [
        ("owner", "Owner"),
        ("shared", "Shared"),
        ("borrowed", "Borrowed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    ownership_type = models.CharField(max_length=20, choices=OWNERSHIP_TYPE, default="owner")
    date_acquired = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user} - {self.car} ({self.ownership_type})"
