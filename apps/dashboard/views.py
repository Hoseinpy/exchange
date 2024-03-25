from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.account.models import CurrencyWallet, IrWallet
from .serializers import IrWalletSerializer, CurrencyWalletSerializer
from rest_framework.permissions import IsAuthenticated


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