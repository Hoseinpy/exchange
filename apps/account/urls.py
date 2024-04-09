from django.urls import path
from .views import(ProfileApiView, ChangePassword, AddCartBankApi, UserCartBankListAPi,
                   AsAllCartBank, AsDetailCartBank)


urlpatterns = [
    path('profile/', ProfileApiView.as_view(), name='profile-api'),
    path('profile/setting/change_password', ChangePassword.as_view(), name='change-password-api'),
    path('profile/user-cart/', UserCartBankListAPi.as_view(), name='user-cart-list-api'),
    path('profile/user-cart/add', AddCartBankApi.as_view(), name='add-cart-api'),
    path('carts/', AsAllCartBank.as_view(), name='cart-bank-list-for-admin-api'),
    path('carts/<str:uuid>', AsDetailCartBank.as_view(), name='cart-bank-detail-for-admin-api'),
]