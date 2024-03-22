from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permission import IsOwnerOrReadOnly
from .serializers import UserSerializer, ChangePasswordSerializer
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model


User = get_user_model()


@method_decorator([csrf_exempt, ratelimit(key='ip', rate='50/m')], name='dispatch')
class ProfileApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = User.objects.filter(email=request.user.email).first()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)
    

@method_decorator([csrf_exempt, ratelimit(key='ip', rate='10/m')], name='dispatch')
class ChangePassword(APIView):
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