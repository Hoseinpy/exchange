from django.shortcuts import render
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import( SingupSerializer, LoginSerializer,
                          ForgetPasswordSerializerStep1,
                          ForgetPasswordSerializerStep2,)
from django.contrib.auth import authenticate
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from utils.send_email import send_email


User = get_user_model()


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='5/m')], name='dispatch')
class SingupApiView(APIView):
    """
    send email and password for create account for user
    """
    def post(self, request):
        serializer = SingupSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(email=serializer.data.get('email'), verify_code=get_random_string(length=72))
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='5/m')], name='dispatch')
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

                response.set_cookie(key='token', value=token, max_age=43200, httponly=True)
                response.data = {
                    'status': 'success',
                }
                return response
            else:
                return Response({'status': 'incorrect email or password'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='4/m')], name='dispatch')
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


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='5/m')], name='dispatch')
class ForgetPasswordApiView(APIView):
    """
    Catch user email and send forget password email
    """
    def post(self, request):
        serializer = ForgetPasswordSerializerStep1(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.data.get('email')).first()
            if user is not None:
                send_email(subject='Forget Password', context={'user': user}, to=serializer.data.get('email'), template_name='user_auth/send_email_body.html')
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'email not found'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='5/m')], name='dispatch')
class ForgetPasswordVerifyAPIView(APIView):
    """
    if user verify code is rigth, user can change password
    """
    def get(self, request, verify_code):
        user = User.objects.filter(verify_code=verify_code).first()
        if user is not None:
            return Response({'status': 'you can change password'}, status=status.HTTP_200_OK)
        return render(request, 'user_auth/404.html') # is render template for developer mode

    def post(self, request, verify_code):
        user = User.objects.filter(verify_code=verify_code).first()
        if user is not None:
            serializer = ForgetPasswordSerializerStep2(data=request.data)
            if serializer.is_valid():
                password = serializer.data.get('password')
                user.set_password(password)
                user.verify_code = get_random_string(72)
                user.save()
                return Response({'status': 'success'}, status=status.HTTP_200_OK)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'verify code is not found'}, status=status.HTTP_404_NOT_FOUND)