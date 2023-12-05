from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import FormView

from products.models import Product
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from cart.cart_module import Cart


def synchronize_wishlist(request):
    if request.user.is_authenticated:
        # Get the products in the session wishlist
        session_wishlist = request.session.get('wishlist', [])

        # Add products from the session wishlist to the user's wishlist
        for product_id in session_wishlist:
            product = get_object_or_404(Product, id=product_id)
            product.wishlist.add(request.user)

        # Clear the session wishlist after synchronizing with the user's wishlist
        request.session['wishlist'] = []

class UserLoginView(FormView):
    def get(self, request):
        cart = Cart(request)
        cart_qty = len(cart)
        if request.user.is_authenticated:
            products_wish = Product.objects.filter(wishlist=request.user)
            wishlist_count = products_wish.count()
        else:
            # For anonymous users, use session to store wishlist items
            wishlist = request.session.get('wishlist', [])
            wishlist_count = len(wishlist)
        form = UserLoginForm()
        return render(request, "profile_users/user_login.html", context={'form': form, 'cart_qty':cart_qty, 'wishlist_count':wishlist_count})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in now")
                synchronize_wishlist(request)
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('/')


            else:
                form.add_error("phone", "invalid username or password")
        else:
            form.add_error("phone", "invalid data")

        return render(request, 'profile_users/user_login.html', {'form': form})


def UserLogOut(request):
    logout(request)
    messages.success(request, "You are logged out now")
    synchronize_wishlist(request)
    return redirect('/')


def is_strong_password(password):
    return password.isalnum() and len(password) >= 8


class UserRegisterView(FormView):
    def get(self, request):
        cart = Cart(request)
        cart_qty = len(cart)
        if request.user.is_authenticated:
            products_wish = Product.objects.filter(wishlist=request.user)
            wishlist_count = products_wish.count()
        else:
            # For anonymous users, use session to store wishlist items
            wishlist = request.session.get('wishlist', [])
            wishlist_count = len(wishlist)
        form = UserRegisterForm()
        return render(request, "profile_users/user_register.html", context={'form': form, 'cart_qty':cart_qty, 'wishlist_count':wishlist_count})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(phone=cd["phone"]).exists():
                form.add_error("phone", "Email or phone number already exists")
            elif not is_strong_password(password=cd["password"]):
                form.add_error("password", "Password must be at least 8 characters long")
            else:
                user = User.objects.create_user(phone=cd["phone"], password=cd["password"])
                authenticated_user = authenticate(request, phone=cd["phone"], password=cd["password"])
                login(request, authenticated_user)
                messages.success(request, "You are logged in now")
                synchronize_wishlist(request)
                return redirect('/')
        else:
            form.add_error("phone", "Invalid data")
        # If there are errors or invalid data, render the registration page
        return render(request, "profile_users/user_register.html", context={'form': form})


class AddAddressView(View):
    def post(self, request):
        form = AddressFormCreation(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
        return render(request, 'profile_users/add_address.html', {'form': form})

    def get(self, request):
        cart = Cart(request)
        cart_qty = len(cart)
        if request.user.is_authenticated:
            products_wish = Product.objects.filter(wishlist=request.user)
            wishlist_count = products_wish.count()
        else:
            # For anonymous users, use session to store wishlist items
            wishlist = request.session.get('wishlist', [])
            wishlist_count = len(wishlist)
        form = AddressFormCreation()
        return render(request, 'profile_users/add_address.html', {'form': form, 'cart_qty':cart_qty, 'wishlist_count':wishlist_count})
