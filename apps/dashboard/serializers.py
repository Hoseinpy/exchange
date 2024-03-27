from rest_framework import serializers

from apps.account.models import CurrencyWallet, IrWallet
from .models import Ticket, TicketAnswer


class CurrencyWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyWallet
        fields = ['name', 'price']


class IrWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrWallet
        fields = ['price']


class TicketAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAnswer
        fields = ['ticket', 'answer', 'created_at']


class TicketSerializer(serializers.ModelSerializer):
    answers = TicketAnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'created_at', 'status', 'answers']