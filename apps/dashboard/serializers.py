from rest_framework import serializers

from apps.account.models import CurrencyWallet
from .models import Ticket, TicketAnswer
from django.contrib.auth import get_user_model


User = get_user_model()


class CurrencyWalletSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    class Meta:
        model = CurrencyWallet
        fields = ['user', 'currency', 'price', 'code']

    def get_user(self, obj):
        return str(obj.user)

    def get_currency(self, obj):
        return str(obj.currency)


class IrWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['balance']


class TicketAnswerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = TicketAnswer
        fields = ['user', 'answer', 'created_at']

    def get_user(self, obj): # TODO: fix
        try:
            if obj.user.first_name:
                return obj.user.first_name + ' ' + obj.user.last_name
            return obj.user.email
        except:
            pass


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


CHOICES = {
    "pending": "pending",
    "open": "open",
    "closed": "closed"
}


class AdminChangeTicketStatusSerializer(serializers.Serializer): # change ticket status
    status = serializers.ChoiceField(choices=CHOICES)