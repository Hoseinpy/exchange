from django.urls import path
from .views import SingupApiView, LoginAPiView, LogoutAPiView, ForgetPasswordApiView, ForgetPasswordVerifyAPIView


urlpatterns = [
    path('singup/', SingupApiView.as_view(), name='singup-api'),
    path('login/', LoginAPiView.as_view(), name='login-api'),
    path('logout/', LogoutAPiView.as_view(), name='logout-api'),
    path('forget-password/', ForgetPasswordApiView.as_view(), name='forget-password-api'),
    path('forget-password/<verify_code>/', ForgetPasswordVerifyAPIView.as_view(), name='forget-password-verify-api'),
]