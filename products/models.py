from django.db import models
from django.db.models import Avg
from django.core.validators import ValidationError, MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericRelation
# from account.models import User
from django.urls import reverse

from profile_users.models import User


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name="subs")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media', blank=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ManyToManyField(Category, blank=True)
    brand = models.ManyToManyField(Brand, blank=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='media')
    size = models.ManyToManyField(Size, verbose_name="products", blank=True)
    color = models.ManyToManyField(Color, verbose_name="products", blank=True)
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    on_sale = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    wishlist = models.ManyToManyField(User, blank=True,related_name="wishlist")

    def __str__(self):
        return self.title


class Review(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50 , default=user)
    email = models.EmailField(blank=True, null=True)
    parents = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="replies")
    body = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=1, blank=True, null=True, validators=[MaxValueValidator(5)])
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.body[:50]

class Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="informations")
    text = models.TextField()

    def __str__(self):
        return self.text