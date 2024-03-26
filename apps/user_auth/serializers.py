from rest_framework import serializers, fields
from django.contrib.auth import get_user_model
from rest_framework import status
from drf_extra_fields.fields import Base64ImageField

User = get_user_model()


class SingupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(max_length=50, required=True, min_length=8)
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


class ForgetPasswordSerializerStep1(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)


class ForgetPasswordSerializerStep2(serializers.Serializer):
    password = serializers.CharField(max_length=50, required=True, min_length=8)
    password2 = serializers.CharField(max_length=50, required=True)

    def validate(self, attrs):

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('password is not match', status.HTTP_400_BAD_REQUEST)

        return attrs


class UserLevel1Serializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, required=True, min_length=10)
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    father_name = serializers.CharField(max_length=30, required=True)
    national_code = serializers.CharField(max_length=10, required=True, min_length=10)


class UserLevel2Serializer(serializers.Serializer):
    image = serializers.ImageField(required=True)