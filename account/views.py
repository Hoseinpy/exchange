from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .permission import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='100/m')], name='dispatch')
class ProfileApiView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()