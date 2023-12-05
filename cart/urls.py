from django.urls import path
from .views import *

app_name = "cart"

urlpatterns = [
    path('detail/', CartDetailView.as_view(),name="cart_detail"),
    path('add/<int:pk>', CartAddView.as_view(), name="cart_add"),
    path('delete/<str:id>', CartDeleteView.as_view(), name="cart_delete"),
    path('order/add', OrderCreationView.as_view(), name="orderadd"),
    path('order/<int:pk>', OrderDetailView.as_view(), name="order_detail"),
    path('applydiscount/<int:pk>', ApplyDiscountCode.as_view(), name="apply_discount"),
    path('purchase', Purchase.as_view(), name="purchase"),
    # path('sendrequest/<int:pk>', PurchaseView.as_view(), name="send_request"),
]