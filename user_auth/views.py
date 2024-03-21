from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from django.conf import settings
from .serializers import SingupSerializer, LoginSerializer, SendEmailSerializer
from django.contrib.auth import authenticate
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

User = get_user_model()


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='10/m')], name='dispatch')
class SingupApiView(APIView):
    """
    send email and password for create account for user
    """
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
class LoginAPiView(APIView):
    """
    send email and password for login to account user
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.data.get('email'), password=serializer.data.get('password'))
            if user is not None:
                token = Token.objects.filter(user=user).first()
                response = Response()

                response.set_cookie(key='token', value=token, max_age=86400, httponly=True)
                response.data = {
                    'status': 'success',
                }
                return response
            else:
                return Response({'status': 'incorrect email or password'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPiView(APIView):
    """
    send request for logout user
    """
    def get(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'status': 'success'
        }
        return response


# todo: add forget password via email