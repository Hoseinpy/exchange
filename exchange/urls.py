from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .mine.btc_price_api import btc_price


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('user_auth.urls')),
    path('api/profile/', include('account.urls')),
    path('api/v1/price/btc', btc_price, name='btc-price-api'),
    path('api/', include('dashboard.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
