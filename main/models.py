from django.db import models

class User(models.Model):
    user_firstname = models.CharField(max_length=200)
    user_lastname = models.CharField(max_length=200)
    car = models.OneToOneField('Car', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user_firstname} {self.user_lastname}"


class Car(models.Model):
    car_brand = models.CharField(max_length=200, default="unknown")
    car_model = models.CharField(max_length=200)
    COLORS = [
        ("black", "Black"),
        ("silver", "Silver"),
        ("white", "White"),
        ("bronze", "Bronze"),
    ]
    car_color = models.CharField(max_length=20, choices=COLORS, default="black")
    car_platenumber = models.IntegerField(unique=True, null=True, blank=True, default="0")

    def __str__(self):
        return f"{self.car_brand} {self.car_model}"
