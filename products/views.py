from profile_users.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from cart.cart_module import Cart
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
import logging

def calculate_average_rate(product):
    reviews = Review.objects.filter(products=product, active=True)
    return reviews.aggregate(Avg('rate'))['rate__avg']


def product_list(request):
    cart = Cart(request)
    cart_qty = len(cart)
    if request.user.is_authenticated:
        products_wish = Product.objects.filter(wishlist=request.user)
        wishlist_count = products_wish.count()
    else:
        # For anonymous users, use session to store wishlist items
        wishlist = request.session.get('wishlist', [])
        wishlist_count = len(wishlist)

    queryset = Product.objects.all().order_by('-created_at')
    recent_products = queryset[:4]
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    brand = request.GET.getlist('brand')
    category = request.GET.getlist('category')
    sort_by = request.GET.get('sort_by')
    on_sale_param = request.GET.get('on_sale')

    if brand:
        queryset = queryset.filter(brand__title__in=brand).distinct()
    if category:
        queryset = queryset.filter(category__title__in=category).distinct()
    if min_price and max_price:
        queryset = queryset.filter(price__lte=max_price, price__gte=min_price)
    elif min_price:
        queryset = queryset.filter(price__gte=min_price)
    elif max_price:
        queryset = queryset.filter(price__lte=max_price)

    if sort_by == 'high_price':
        queryset = queryset.order_by('-price')
    elif sort_by == 'low_price':
        queryset = queryset.order_by('price')
    elif sort_by == 'on_sale_product':
        queryset = queryset.filter(on_sale=True)

    if on_sale_param == 'true':
        queryset = queryset.filter(on_sale=True)

    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page')
    objects_list = paginator.get_page(page_number)
    return render(request, 'products/product_list.html',
                  context={'products': objects_list, 'recent_products': recent_products, 'cart_qty': cart_qty,
                           'wishlist_count': wishlist_count})


def Product_Detail(request, title):
    cart = Cart(request)
    cart_qty = len(cart)
    if request.user.is_authenticated:
        products_wish = Product.objects.filter(wishlist=request.user)
        wishlist_count = products_wish.count()
    else:
        wishlist = request.session.get('wishlist', [])
        wishlist_count = len(wishlist)
    products = get_object_or_404(Product, title=title)
    comments = Review.objects.filter(products=products, active=True)
    category = Category.objects.all()
    related_products = Product.objects.filter(category__in=products.category.all()).exclude(
        id=products.id)[:4]
    if request.method == "POST":
        body = request.POST.get("body")
        email = request.POST.get("email")
        name = request.POST.get("name")
        rate = request.POST.get("rate")
        Review.objects.create(body=body, email=email, name=name, rate=rate, products=products, user=request.user)
        return redirect("product:product_detail", title=title)

    average_rate = calculate_average_rate(products)
    # paginator = Paginator(comments, 4)
    # page = request.GET.get('page')
    #
    # try:
    #     comments = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     comments = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     comments = paginator.page(paginator.num_pages)
    return render(request, 'products/product_detail.html',
                  context={'products': products, 'comments': comments, 'average_rate': average_rate,
                           'category': category, 'related_products': related_products, 'cart_qty': cart_qty,
                           'wishlist_count': wishlist_count})


def Search(request):
    cart = Cart(request)
    cart_qty = len(cart)
    if request.user.is_authenticated:
        products_wish = Product.objects.filter(wishlist=request.user)
        wishlist_count = products_wish.count()
    else:
        wishlist = request.session.get('wishlist', [])
        wishlist_count = len(wishlist)
    q = request.GET.get('q')
    products = Product.objects.filter(title__icontains=q)
    page_number = request.GET.get('page')
    paginator = Paginator(products, 3)
    objects_list = paginator.get_page(page_number)
    return render(request, 'products/product_list.html',
                  context={'products': objects_list, 'cart_qty': cart_qty, 'wishlist_count': wishlist_count})


def category_product(request, category_title):
    cart = Cart(request)
    cart_qty = len(cart)
    if request.user.is_authenticated:
        products_wish = Product.objects.filter(wishlist=request.user)
        wishlist_count = products_wish.count()
    else:
        wishlist = request.session.get('wishlist', [])
        wishlist_count = len(wishlist)
    category = Category.objects.get(title=category_title)
    recent_products = Product.objects.all().order_by('-created_at')[:4]
    # Count the number of products in the category
    products = Product.objects.filter(category=category).annotate(product_count=Count('id'))
    # Get the product count for the category
    product_count = Product.objects.filter(category=category).count()
    context = {
        'categories': Category.objects.all(),
        'products': products,
        'product_count': product_count,
        'recent_products': recent_products,
        'cart_qty': cart_qty,
        'wishlist_count': wishlist_count
    }
    return render(request, 'products/product_list.html', context)



def wishlist(request):
    cart = Cart(request)
    cart_qty = len(cart)

    if request.user.is_authenticated:
        products_wish = Product.objects.filter(wishlist=request.user)
        wishlist_count = products_wish.count()
    else:
        # For anonymous users, use session to store wishlist items
        wishlist = request.session.get('wishlist', [])
        wishlist_count = len(wishlist)
        products_wish = Product.objects.filter(id__in=wishlist)

    return render(request, 'products/user_wishlist.html',
                  context={'products': products_wish, 'wishlist_count': wishlist_count, 'cart_qty': cart_qty})



def add_wishlist(request, id):
    product = get_object_or_404(Product, id=id)

    if request.user.is_authenticated:
        if product.wishlist.filter(id=request.user.id).exists():
            product.wishlist.remove(request.user)
            messages.success(request, f"Product {product.title} removed from your wishlist")
        else:
            product.wishlist.add(request.user)
            messages.success(request,
                             f'Product {product.title} added to your wishlist. <a href="{reverse("product:wishlist")}" class="alert-link">Your Wishlist</a>')
    else:
        # For anonymous users, use session to store wishlist items
        wishlist = request.session.get('wishlist', [])
        if product.id not in wishlist:
            wishlist.append(product.id)
            messages.success(request, f'Product {product.title} added to your wishlist.')
        else:
            wishlist.remove(product.id)
            messages.success(request, f"Product {product.title} removed from your wishlist")

        # Save the updated wishlist back to the session
        request.session['wishlist'] = wishlist

    # Redirect to the previous page or a specific URL
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("product:wishlist")))


def go_to_gateway_view(request):
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = 1000
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = '+989112221234'  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create()  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('callback-gateway'))
        bank.set_mobile_number(user_mobile_number)  # اختیاری

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()

        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e