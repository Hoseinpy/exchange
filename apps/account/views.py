from django.http import Http404
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import (AllCartBankSeralizer, UserSerializer, ChangePasswordSerializer,
                           CartBankModelSerializer, RejectOrAcceptSeralizer)
from .models import CartBankModel
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination


User = get_user_model()


class ProfileApiView(APIView):
    """
    show all info about user
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = User.objects.filter(email=request.user.email).first()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)
    

@method_decorator([csrf_exempt], name='dispatch')
class ChangePassword(APIView):
    """
    this for change password api
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=request.user.email).first()
            current_password = serializer.data.get('current_password')
            if user.check_password(current_password):
                password = serializer.data.get('password')
                user.set_password(password)
                user.save()
                return Response({'status': 'success'}, status.HTTP_200_OK)
            else:
                return Response({'status': 'current_password is not Right!!'}, status.HTTP_404_NOT_FOUND)
            
        return Response({'status': 'bad request'}, status.HTTP_400_BAD_REQUEST)


class UserCartBankListAPi(APIView):
    """
    show all user bank cart
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_bank = CartBankModel.objects.filter(user=request.user).filter(is_accepted=True)
        serializer = CartBankModelSerializer(cart_bank, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class AddCartBankApi(APIView):
    """
    add cart bank if user is level 1 or gt
    """
    permission_classes = [IsAuthenticated]

    def post(self, request): # !!
        user = request.user
        if user.user_level > 'Level0':
            serializer = CartBankModelSerializer(data=request.data)
            if serializer.is_valid():
                cart_number = serializer.data.get('cart_number')
                if CartBankModel.objects.filter(user=user).filter(cart_number=cart_number).exists():
                    return Response({'status': 'this cart-number is already exists'}, status.HTTP_302_FOUND)
                
                cart = CartBankModel(user=request.user, cart_number=cart_number)
                cart.save()
                return Response({'status': 'Success, the admin accepts or rejects'}, status.HTTP_201_CREATED) # TODO: in status message add 'You will be notified by email'

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'you need to complete level 1 for add cart-bank'}, status.HTTP_406_NOT_ACCEPTABLE)
    

class AsAllCartBank(generics.ListAPIView):
    """
    show all is_accepted=False in CartBank model for admin
    """
    class PagenationSetting(PageNumberPagination):
        page_size = 10

    serializer_class = AllCartBankSeralizer
    queryset = CartBankModel.objects.filter(is_accepted=False).order_by('-created_at')
    permission_classes = [IsAdminUser]
    pagination_class = PagenationSetting


class AsDetailCartBank(APIView):
    permission_classes = [IsAdminUser]

    def get_cart_bank(self, uuid):
        cart = CartBankModel.objects.filter(uuid__iexact=uuid).first()
        if cart:
            return cart
        else:
            raise Http404()

    def get(self, request, uuid):
        cart = self.get_cart_bank(uuid)
        serializer = AllCartBankSeralizer(cart)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, uuid):
        serializer = RejectOrAcceptSeralizer(data=request.data)
        if serializer.is_valid():
            admin_choice = serializer.data.get('admin_choice')
            cart = self.get_cart_bank(uuid)
            
            if admin_choice == 'accept':
                cart.is_accepted = True
                cart.save()
                return Response({'status': 'ok'}, status.HTTP_200_OK)
            
            elif admin_choice == 'reject':

                # TODO: Ability to add text to reject the request in AS
                cart.delete()
                return Response({'status': 'ok'}, status.HTTP_200_OK)
            
            else:
                return Response({'status': 'choice is not valid'}, status.HTTP_406_NOT_ACCEPTABLE)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)