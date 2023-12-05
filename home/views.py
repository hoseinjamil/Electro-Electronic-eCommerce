from django.shortcuts import render, get_object_or_404, redirect
from products.models import *
from .foms import NewsletterForm
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from cart.cart_module import Cart


def home(request):
    cart = Cart(request)
    cart_qty = len(cart)
    if request.user.is_authenticated:
        products_wish = Product.objects.filter(wishlist=request.user)
        wishlist_count = products_wish.count()
    else:
        # For anonymous users, use session to store wishlist items
        wishlist = request.session.get('wishlist', [])
        wishlist_count = len(wishlist)
    products = Product.objects.all()
    recent_products = Product.objects.all().order_by('-created_at')
    widget_products1 = Product.objects.all()[:6]
    widget_products2 = Product.objects.all()[7:12]
    widget_recent_products2 = Product.objects.all().order_by('-created_at')[0:6]
    categories = Category.objects.all()
    off_products = Product.objects.filter(on_sale=True)

    return render(request, 'home/index.html', context={
        'products': products, 'recent_products': recent_products, 'widget_products1': widget_products1,
        'widget_products2': widget_products2, 'widget_recent_products2': widget_recent_products2,
        'categories': categories, 'off_products': off_products, 'cart_qty':cart_qty, 'wishlist_count':wishlist_count})


def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            Newsletter.objects.create(email=email)
            messages.success(request, "Your email has been subscribed now")
            return render(request, 'home/index.html', context={'form': form})
    else:
        form = NewsletterForm()
    return render(request, 'home/index.html', {'form': form})
