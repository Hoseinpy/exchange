from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .mine.currency_price import currency_price


urlpatterns = [
    path('admin/', admin.site.urls), # dj admin
    path('api/auth/', include('apps.user_auth.urls')),
    path('api/', include('apps.account.urls')),
    path('api/v1/price/<str:name>', currency_price, name='currency-price-api'),
    path('api/dashboard/', include('apps.dashboard.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
