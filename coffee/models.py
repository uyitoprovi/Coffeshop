from django.db import models
from django.contrib.auth.models import User


class Coffee(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.CharField(max_length=2083)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
