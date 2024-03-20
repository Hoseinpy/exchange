from django.urls import path
from .views import SingupApiView


urlpatterns = [
    path('singup/', SingupApiView.as_view(), name='singup-api')
]