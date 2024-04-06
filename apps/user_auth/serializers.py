from rest_framework import serializers, fields
from django.contrib.auth import get_user_model
from rest_framework import status
from django_recaptcha.fields import ReCaptchaField # i dont know is work or not
from .models import AsUserLevel1CheckModel, AsUserLevel2CheckModel


User = get_user_model()


class ReCaptchaSerializer(ReCaptchaField):  # i dont know is work or not
    default_error_messages = {
        "invalid-input-response": "reCAPTCHA token is invalid.",
    }


class SingupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(max_length=50, required=True, min_length=8)
    password2 = serializers.CharField(max_length=50, required=True)
    captcha = ReCaptchaSerializer()  # i dont know is work or not

    def validate(self, attrs):

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('password is not match', status.HTTP_400_BAD_REQUEST)

        elif User.objects.filter(email__iexact=attrs['email']).exists():
            raise serializers.ValidationError('email is already take', status.HTTP_400_BAD_REQUEST)

        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(max_length=50, required=True)
    captcha = ReCaptchaSerializer()  # i dont know is work or not


class ForgetPasswordSerializerStep1(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)
    captcha = ReCaptchaSerializer()  # i dont know is work or not


class ForgetPasswordSerializerStep2(serializers.Serializer):
    password = serializers.CharField(max_length=50, required=True, min_length=8)
    password2 = serializers.CharField(max_length=50, required=True)
    captcha = ReCaptchaSerializer()  # i dont know is work or not

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
    authentication_image = serializers.ImageField(required=True)


class AllLevel1InfoSeralizer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = AsUserLevel1CheckModel
        fields = ['user', 'created_at']

    def get_user(self, obj):
        return obj.user.email
    

class DetailLevel1InfoSeralizer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = AsUserLevel1CheckModel
        fields = ['user', 'first_name', 'last_name', 'father_name', 'national_code', 'phone_number', 'created_at']

    def get_user(self, obj):
        return obj.user.email


class AllLevel2InfoSeralizer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = AsUserLevel1CheckModel
        fields = ['user', 'created_at']

    def get_user(self, obj):
        return obj.user.email


class DetailLevel2InfoSeralizer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = AsUserLevel2CheckModel
        fields = ['user', 'authentication_image', 'created_at']

    def get_user(self, obj):
        return obj.user.email