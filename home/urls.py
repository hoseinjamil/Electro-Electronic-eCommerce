from django.urls import path
from . import views
from products.views import category_product

app_name = "home"

urlpatterns = [
    path("", views.home, name="home"),
    path("", views.newsletter, name="newsletter"),
    path('category_product/<str:category_title>/', category_product, name='category_product'),
]
