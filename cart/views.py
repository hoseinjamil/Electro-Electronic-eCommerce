import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .cart_module import Cart
from .models import *
from django.contrib import messages
from django.urls import reverse



class CartDetailView(LoginRequiredMixin, View):
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
        is_cart_empty = cart_qty == 0
        return render(request, 'cart/cart_detail.html', context={'cart': cart, 'cart_qty': cart_qty, 'is_cart_empty': is_cart_empty, 'wishlist_count':wishlist_count})


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        size, color, quantity = request.POST.get("size", "Empty"), request.POST.get("color", "Empty"), request.POST.get(
            "quantity")
        cart = Cart(request)
        cart_qty = len(cart)
        cart.add(product, quantity, color, size)
        print(size, color, quantity)
        messages.success(request, f'Product {product.title} added to your cart. <a href="{reverse("cart:cart_detail")}" class="alert-link">Your Cart</a>')
        return redirect("cart:cart_detail")


class CartDeleteView(View):
    def get(self, request, id):
        print(id)
        cart = Cart(request)
        cart.delete(id)
        cart_qty = len(cart)
        messages.success(request, 'product has been removed' )
        return redirect("cart:cart_detail")


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        products_wish = Product.objects.filter(wishlist=request.user)
        wishlist_count = products_wish.count()
        order = get_object_or_404(Order, id=pk)
        return render(request, 'cart/order_detail.html', {'order': order, 'wishlist_count':wishlist_count})


class OrderCreationView(LoginRequiredMixin, View):
    def get(get, request):
        cart = Cart(request)

        order = Order.objects.create(user=request.user, total_price=cart.total())
        for item in cart:
            Orderitem.objects.create(order=order, product=item['product'], color=item['color'], size=item['size'],
                                     quantity=item['quantity'], price=item['price'])

        cart.remove_cart()
        return redirect('cart:order_detail', order.id)




class ApplyDiscountCode(LoginRequiredMixin, View):
    def post(self, request, pk):
        code = request.POST.get('discount_code')
        order = get_object_or_404(Order, id=pk)

        # Check if the discount code has already been used for this order
        if order.discount_codes.filter(name=code).exists():
            return render(request, 'cart/order_detail.html', {
                'order': order,
                'already_used': True,
            })

        discount_code = get_object_or_404(DiscountCode, name=code)

        expired = discount_code.is_expired()
        quantity_finished = discount_code.quantity == 0

        if expired or quantity_finished:
            return render(request, 'cart/order_detail.html', {
                'order': order,
                'expired': expired,
                'quantity_finished': quantity_finished,
            })

        order.total_price -= order.total_price * discount_code.discount / 100
        order.save()
        order.discount_codes.add(discount_code)  # Add the discount code to the order's used discount codes
        discount_code.quantity -= 1
        discount_code.save()  # Decrease the quantity of the discount code
        return redirect('cart:order_detail', order.id)



class Purchase(View):
    def get(self,request):
        cart = Cart(request)
        cart_qty = len(cart)
        if request.user.is_authenticated:
            products_wish = Product.objects.filter(wishlist=request.user)
            wishlist_count = products_wish.count()
        else:
            # For anonymous users, use session to store wishlist items
            wishlist = request.session.get('wishlist', [])
            wishlist_count = len(wishlist)


        user_phone = request.user.phone
        return render(request, 'cart/purchase.html', context={'cart_qty':cart_qty, 'wishlist_count':wishlist_count, 'user_phone':user_phone})
