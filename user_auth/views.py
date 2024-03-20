from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from .serializers import SingupSerializer

User = get_user_model()


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