from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('account/login', views.UserLoginView.as_view(), name="user_login"),
    path('account/logout', views.UserLogOut, name="user_logout"),
    path('account/register', views.UserRegisterView.as_view(), name="user_register"),
    path('account/add/address', views.AddAddressView.as_view(), name="add_address"),
]
