from django.shortcuts import render
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import( SingupSerializer, LoginSerializer,
                          ForgetPasswordSerializerStep1,
                          ForgetPasswordSerializerStep2,
                          UserLevel1Serializer,
                          UserLevel2Serializer)
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from utils.send_email import send_email


User = get_user_model()


@method_decorator([csrf_exempt], name='dispatch')
class SingupApiView(APIView):
    """
    send email and password for create account to user
    """
    def post(self, request):
        serializer = SingupSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(email=serializer.data.get('email'),
                                        verify_code=get_random_string(72))
            
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator([csrf_exempt], name='dispatch')
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

                response.set_cookie(key='token', value=token, max_age=4320, httponly=True)
                response.data = {
                    'status': 'success',
                }
                return response
            else:
                return Response({'status': 'incorrect email or password'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator([csrf_exempt], name='dispatch')
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


@method_decorator([csrf_exempt], name='dispatch')
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


@method_decorator([csrf_exempt], name='dispatch')
class ForgetPasswordVerifyAPIView(APIView):
    """
    if user verify code is rigth, user can change password
    """
    def get(self, request, verify_code):
        user = User.objects.filter(verify_code=verify_code).first()
        if user is not None:
            return Response({'status': 'you can change password'}, status=status.HTTP_200_OK)
        return render(request, 'user_auth/404.html') # the render template for developer mode

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


@method_decorator([csrf_exempt], name='dispatch')
class UserLevel1ApiView(APIView):
    """
    user send f_name, l_name, father_name and national_code to up level user for 1
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserLevel1Serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=request.user.email).first()
            if user.first_name and user.last_name and user.father_name and user.national_code and user.phone_number:
                return Response({'status': 'you already in level 1'}, status=status.HTTP_208_ALREADY_REPORTED)
            else:
                if User.objects.filter(phone_number=serializer.data.get('phone_number'), national_code=serializer.data.get('national_code')).exists():
                    return Response({'status': 'phone_number or national_code is already registered'}, status=status.HTTP_208_ALREADY_REPORTED)
                else:
                    user.phone_number = serializer.data.get('phone_number')
                    user.first_name = serializer.data.get('first_name')
                    user.last_name = serializer.data.get('last_name')
                    user.father_name = serializer.data.get('father_name')
                    user.national_code = serializer.data.get('national_code')
                    user.user_level = 1
                    user.save()
                    return Response({'status': 'success'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator([csrf_exempt], name='dispatch')
class UserLevel2ApiView(APIView):
    """
    user send authentication image to up level user for 2
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserLevel2Serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=request.user.email).first()
            if user.user_level == '1':
                """
                if user is level 1 can go level 2
                """
                if user.authentication_image and user.is_authentication:
                    return Response({'status': 'you already in level 2'}, status=status.HTTP_208_ALREADY_REPORTED)
                else:
                    user.authentication_image = request.data.get('image')
                    user.is_authentication = True
                    user.user_level = 2
                    user.save()
                    return Response({'status': 'success'}, status=status.HTTP_200_OK)

            return Response({'status': 'you need to complete level 1 to go level 2'}, status.HTTP_510_NOT_EXTENDED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator([csrf_exempt], name='dispatch')
class UserLevel3APiView(APIView):
    permission_classes = [IsAuthenticated]

    """
    if user total buy is 1500$ user can go level 3
    """
    def post(self, request):
        pass