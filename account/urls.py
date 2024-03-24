from django.urls import path
from .views import ProfileApiView, ChangePassword, AddCartBankApi, UserCartBankListAPi


urlpatterns = [
    path('profile/', ProfileApiView.as_view(), name='profile-api'),
    path('setting/change_password', ChangePassword.as_view(), name='change-password-api'),
    path('user-cart/', UserCartBankListAPi.as_view(), name='user-cart-list-api'),
    path('user-cart/add', AddCartBankApi.as_view(), name='add-cart-api'),
]