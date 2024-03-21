from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class SingupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(max_length=50, required=True)
    password2 = serializers.CharField(max_length=50, required=True)

    def validate(self, attrs):

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('password is not match', status.HTTP_400_BAD_REQUEST)

        elif User.objects.filter(email__iexact=attrs['email']).exists():
            raise serializers.ValidationError('email is already take', status.HTTP_400_BAD_REQUEST)

        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(max_length=50, required=True)
