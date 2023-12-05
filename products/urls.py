from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path('product-detail/<str:title>', views.Product_Detail, name="product_detail"),
    path('category/<str:category_title>/', views.category_product, name='filtered_product_list'),
    path('products', views.product_list, name="product_list"),
    path('search', views.Search, name="search"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('add_wishlist/<int:id>/', views.add_wishlist, name="add_wishlist"),
    path('go-to-gateway/', views.go_to_gateway_view, name="gateway"),

]
