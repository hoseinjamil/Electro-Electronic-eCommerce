from django.shortcuts import render
from products.models import Product
from cart.cart_module import Cart
from .forms import *
from .models import *
from django.contrib import messages


def Contact(request):
    cart = Cart(request)
    cart_qty = len(cart)
    if request.user.is_authenticated:
        products_wish = Product.objects.filter(wishlist=request.user)
        wishlist_count = products_wish.count()
    else:
        # For anonymous users, use session to store wishlist items
        wishlist = request.session.get('wishlist', [])
        wishlist_count = len(wishlist)
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            ContactUs.objects.create(name=name, email=email, subject=subject, body=body)
            messages.success(request, "Your message has been sent")
            return render(request, 'contact/contact.html', context={'form': form})
    else:
        form = ContactUsForm()

    return render(request, 'contact/contact.html', context={'form': form, 'cart_qty':cart_qty, 'wishlist_count':wishlist_count})
