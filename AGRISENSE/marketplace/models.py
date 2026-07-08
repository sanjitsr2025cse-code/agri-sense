from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    is_seller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

class CropListing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    expected_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='crop_images/')
    created_at = models.DateTimeField(auto_now_add=True)

class PriceHistory(models.Model):
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    market = models.CharField(max_length=100)
    commodity = models.CharField(max_length=100)
    variety = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
