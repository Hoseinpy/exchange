import uuid
from django.http import Http404
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from utils.send_email import send_email
from rest_framework.response import Response
from rest_framework import status, generics

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from apps.account.serializers import RejectOrAcceptSeralizer, RejectTextSeralizer
from .models import AsUserLevel1CheckModel, AsUserLevel2CheckModel

from .serializers import( SingupSerializer, LoginSerializer, ForgetPasswordSerializerStep1,
                          ForgetPasswordSerializerStep2, UserLevel1Serializer, UserLevel2Serializer,
                          AllLevel1InfoSeralizer, DetailLevel1InfoSeralizer, AllLevel2InfoSeralizer, 
                          DetailLevel2InfoSeralizer)

# get user model
User = get_user_model()


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='5/m')], name='dispatch')
class SingupApiView(APIView):
    """
    send email and password for create account to user
    """
    def post(self, request):
        serializer = SingupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            if User.objects.filter(email=email).exists():
                return Response({'status': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(email=email,
                                        verify_code=get_random_string(72))
            
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

                response.set_cookie(key='token', value=token, max_age=4320, httponly=True, secure=True) # add secure option
                response.data = {
                    'status': 'success',
                }
                return response
            else:
                return Response({'status': 'incorrect email or password'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='3/m')], name='dispatch')
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


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='10/m')], name='dispatch')
class UserLevel1ApiView(APIView):
    """
    user send information for up level 0 --> 1 
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserLevel1Serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=request.user.email).first()
            if user.user_level == 'Level1':
                return Response({'status': 'you already complite level 1'}, status=status.HTTP_302_FOUND)
            
            national_code = serializer.data.get('national_code')
            phone_number = serializer.data.get('phone_number')

            if User.objects.filter(national_code=national_code, phone_number=phone_number).exists():
                return Response({'status': 'phone number or national code is exists'}, status=status.HTTP_400_BAD_REQUEST)

            if AsUserLevel1CheckModel.objects.filter(user=user).exists():
                return Response({'status': 'You have already submitted your information, you cannot submit again until your request is rejected'}, status=status.HTTP_208_ALREADY_REPORTED)
                
            as_level = AsUserLevel1CheckModel(
                user = user,
                first_name = serializer.data.get('first_name'),
                last_name = serializer.data.get('last_name'),
                father_name = serializer.data.get('father_name'),
                national_code = national_code,
                phone_number = phone_number,
                uuid= str(uuid.uuid4())[:15]
            )
            as_level.save()
            return Response({'status': 'Success, the admin accepts or rejects, You will be notified by email'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='10/m')], name='dispatch')
class UserLevel2ApiView(APIView):
    """
    user send information for up level 1 --> 2
    """
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = UserLevel2Serializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.filter(email=request.user.email).first()
            if user.user_level >= 'Level1': # if user is level1 can continue

                if user.user_level == 'Level2':
                    return Response({'status': 'you already complite level 2'}, status=status.HTTP_208_ALREADY_REPORTED)
                
                authentication_image = request.FILES['authentication_image']

                if AsUserLevel2CheckModel.objects.filter(user=user).exists():
                    return Response({'status': 'You have already submitted your information, you cannot submit again until your request is rejected'}, status=status.HTTP_208_ALREADY_REPORTED)
                
                as_level = AsUserLevel2CheckModel(
                    user = user,
                    authentication_image = authentication_image,
                    uuid= str(uuid.uuid4())[:15]
                )
                as_level.save()

                return Response({'status': 'Success, the admin accepts or rejects, You will be notified by email'}, status=status.HTTP_200_OK)

            return Response({'status': 'you need to complete level 1 to go level 2'}, status.HTTP_510_NOT_EXTENDED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@method_decorator([csrf_exempt, ratelimit(key='ip', rate='10/m')], name='dispatch')
class UserLevel3APiView(APIView):
    permission_classes = [IsAuthenticated]

    """
    if user total buy and sell is 1500$ user can go level 3
    """
    def post(self, request):
        pass


class AsAllLevel1Info(generics.ListAPIView):
    """
    show all level 1 requests info for admin
    """
    class PagenationSetting(PageNumberPagination):
        page_size = 10

    serializer_class = AllLevel1InfoSeralizer
    queryset = AsUserLevel1CheckModel.objects.filter(is_accepted=False).order_by('-created_at')
    permission_classes = [IsAdminUser]
    pagination_class = PagenationSetting


class AsDetailLevel1Info(APIView):
    """
    admin see more info about request and can accept or reject it
    """
    permission_classes = [IsAdminUser]

    def get_level1_info(self, uuid):
        if user_info := AsUserLevel1CheckModel.objects.filter(uuid__iexact=uuid).first():
            return user_info
        else:
            raise Http404()

    def get(self, request, uuid):
        user_info = self.get_level1_info(uuid)
        serializer = DetailLevel1InfoSeralizer(user_info)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, uuid):
        serializer = RejectOrAcceptSeralizer(data=request.data)
        if serializer.is_valid():
            admin_choice = serializer.data.get('admin_choice')
            user_info = self.get_level1_info(uuid)
            
            if admin_choice == 'accept':
                user = User.objects.filter(email=user_info.user).first()

                user_info.is_accepted = True
                user.first_name = user_info.first_name
                user.last_name = user_info.last_name
                user.father_name = user_info.father_name
                user.national_code = user_info.national_code
                user.phone_number = user_info.phone_number
                user.user_level = 'Level1'
                
                user.save()
                user_info.save()
                return Response({'status': 'ok'}, status.HTTP_200_OK)
            
            elif admin_choice == 'reject':
                serializerr = RejectTextSeralizer(data=request.data)
                if serializerr.is_valid():
                    admin_text = serializerr.data.get('text')
                    send_email(subject='request for up user level to 1 was rejected', context={'text': admin_text, 'user':user_info.user}, to=user_info.user.email, template_name='user_auth/level1_reject.html')
                    user_info.delete()
                    return Response({'status': 'ok'}, status.HTTP_200_OK)
                
                return Response(serializerr.errors, status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'status': 'choice is not valid'}, status.HTTP_406_NOT_ACCEPTABLE)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class AsAllLevel2Info(generics.ListAPIView):
    """
    show all level 2 requests info for admin
    """
    class PagenationSetting(PageNumberPagination):
        page_size = 10

    serializer_class = AllLevel2InfoSeralizer
    queryset = AsUserLevel2CheckModel.objects.filter(is_accepted=False).order_by('-created_at')
    permission_classes = [IsAdminUser]
    pagination_class = PagenationSetting


class AsDetailLevel2Info(APIView):
    """
    admin see more info about request and can accept or reject it
    """
    permission_classes = [IsAdminUser]

    def get_level2_info(self, uuid):
        if user_info := AsUserLevel2CheckModel.objects.filter(uuid__iexact=uuid).first():
            return user_info
        else:
            raise Http404()

    def get(self, request, uuid):
        user_info = self.get_level2_info(uuid)
        serializer = DetailLevel2InfoSeralizer(user_info)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, uuid):
        serializer = RejectOrAcceptSeralizer(data=request.data)
        if serializer.is_valid():
            admin_choice = serializer.data.get('admin_choice')
            user_info = self.get_level2_info(uuid)

            if admin_choice == 'accept':
                user = User.objects.filter(email=user_info.user).first()

                user_info.is_accepted = True
                user.authentication_image = user_info.authentication_image
                user.is_authentication = True
                user.user_level = 'Level2'
                
                user.save()
                user_info.save()
                return Response({'status': 'ok'}, status.HTTP_200_OK)

            elif admin_choice == 'reject':
                serializerr = RejectTextSeralizer(data=request.data)
                if serializerr.is_valid():
                    admin_text = serializerr.data.get('text')
                    send_email(subject='request for up user level to 2 was rejected', context={'text': admin_text, 'user':user_info.user}, to=user_info.user.email, template_name='user_auth/level2_reject.html')
                    user_info.delete()
                    
                    return Response({'status': 'ok'}, status.HTTP_200_OK)
                
                return Response(serializerr.errors, status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'status': 'choice is not valid'}, status.HTTP_406_NOT_ACCEPTABLE)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)