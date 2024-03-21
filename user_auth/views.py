from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from .serializers import SingupSerializer, LoginSerializer
from django.contrib.auth import authenticate, login, logout
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='10/m')], name='dispatch')
class SingupApiView(APIView):
    def post(self, request):
        serializer = SingupSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(email=serializer.data.get('email'))
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='8/m')], name='dispatch')
class LoginAPiView(APIView): # todo: add user token to header
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.data.get('email'), password=serializer.data.get('password'))
            if user is not None:
                login(request, user)
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'incorrect email or password'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)