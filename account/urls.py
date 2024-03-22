from django.urls import path
from .views import ProfileApiView, ChangePassword


urlpatterns = [
    path('profile/', ProfileApiView.as_view(), name='profile-api'),
    path('setting/change_password', ChangePassword.as_view(), name='change-password-api'),
]