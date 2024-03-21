from django.urls import path
from .views import SingupApiView, LoginAPiView

urlpatterns = [
    path('singup/', SingupApiView.as_view(), name='singup-api'),
    path('login/', LoginAPiView.as_view(), name='login-api'),
]