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
    user = serializers.SerializerMethodField()

    class Meta:
        model = TicketAnswer
        fields = ['user', 'answer', 'created_at']

    def get_user(self, obj):
        try:
            return obj.user.first_name + ' ' + obj.user.last_name
        except:
            return obj.user


class TicketListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['user', 'title', 'status', 'created_at']

    def get_user(self, obj):
        try:
            return obj.user.first_name + ' ' + obj.user.last_name
        except:
            return obj.user.email


class TicketDetailSerializer(serializers.ModelSerializer):
    answers = TicketAnswerSerializer(read_only=True, many=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['user', 'title', 'description', 'created_at', 'status', 'answers']

    def get_user(self, obj):
        try:
            return obj.user.first_name + ' ' + obj.user.last_name
        except:
            return obj.user.email