from django.urls import path
from .views import SingupApiView, LoginAPiView, LogoutAPiView


urlpatterns = [
    path('singup/', SingupApiView.as_view(), name='singup-api'),
    path('login/', LoginAPiView.as_view(), name='login-api'),
    path('logout/', LogoutAPiView.as_view(), name='logout-api'),
]