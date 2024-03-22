from django.urls import path
from .views import ProfileApiView


urlpatterns = [
    path('profile/<int:pk>', ProfileApiView.as_view(), name='profile-api')
]