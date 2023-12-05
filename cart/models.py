from django.db import models
from django.conf import settings
from products.models import *
from django.utils import timezone


class DiscountCode(models.Model):
    name = models.CharField(max_length=20, unique=True)
    discount = models.SmallIntegerField(default=0)
    quantity = models.SmallIntegerField(default=1)
    expire_date = models.DateField(null=True, blank=True)

    def is_expired(self):
        if self.expire_date is not None:
            return timezone.now().date() > self.expire_date
        return False

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    total_price = models.IntegerField(default=0)
    phone = models.CharField(max_length=12)
    created = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    discount_codes = models.ManyToManyField(DiscountCode, related_name='orders')

    def __str__(self):
        return self.phone


class Orderitem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    size = models.CharField(max_length=120)
    color = models.CharField(max_length=120)
    quantity = models.SmallIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.order.phone