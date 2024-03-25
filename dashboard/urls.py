from django.urls import path
from .views import CurrencyWalletView, IrWalletView


urlpatterns = [
    path('real-wallet/', IrWalletView.as_view(), name='real-wallet-api'),
    path('currency-wallet/',CurrencyWalletView.as_view(), name='currency-wallet-api')
]
