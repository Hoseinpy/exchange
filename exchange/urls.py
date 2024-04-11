from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .mine.currency_price import currency_price
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Documenting API')


urlpatterns = [
    path('admin/', admin.site.urls), # django admin
    
    path('api/auth/', include('apps.user_auth.urls')),
    path('api/', include('apps.account.urls')),
    path('api/v1/price/<str:name>', currency_price, name='currency-price-api'),
    path('api/dashboard/', include('apps.dashboard.urls')),

    # Documenting API
    path('documenting/api', schema_view, name='Documenting-API'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
