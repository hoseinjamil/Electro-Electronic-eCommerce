from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from azbankgateways.urls import az_bank_gateways_urls

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include("home.urls")),
                  path('', include("products.urls")),
                  path('', include("profile_users.urls")),
                  path('', include("contact.urls")),
                  path('cart/', include("cart.urls")),
                  path('accounts/', include("allauth.urls")),
                  path('bankgateways/', az_bank_gateways_urls()),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
