from django.urls import path
from .views import CurrencyWalletView, IrWalletView


urlpatterns = [
    path('', IrWalletView.as_view(), name='real-pending'),
    path('currency/',CurrencyWalletView.as_view(), name='currency-pending')
]