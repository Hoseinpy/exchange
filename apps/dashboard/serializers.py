from rest_framework import serializers

from apps.account.models import CurrencyWallet, IrWallet


class CurrencyWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyWallet
        fields = ['name', 'price']


class IrWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrWallet
        fields = ['price']