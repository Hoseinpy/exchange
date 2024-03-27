from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from apps.account.models import CurrencyWallet, IrWallet
from .models import Ticket
from .permission import IsOwnerOrAdmin
from .serializers import IrWalletSerializer, CurrencyWalletSerializer, TicketSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model


User = get_user_model()


class IrWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallets = IrWallet.objects.filter(user=request.user).first()
        serializer = IrWalletSerializer(wallets)
        return Response(serializer.data, status.HTTP_200_OK)


class CurrencyWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallets = CurrencyWallet.objects.filter(user=request.user).first()
        serializer = CurrencyWalletSerializer(wallets)
        return Response(serializer.data, status.HTTP_200_OK)


class TicketListForAdminApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        tickets = Ticket.objects.all().order_by('-created_at')
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TicketListForOwnerApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TicketAddApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            ticket = Ticket.objects.create(user=request.user, title=serializer.validated_data['title'], description=serializer.validated_data['description'], status='new')
            return Response({'statsu': 'success'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketDetailApiView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    queryset = Ticket.objects.all().order_by('-created_at')
    serializer_class = TicketSerializer

