from rest_framework import serializers
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import CartBankModel

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'father_name', 'national_code', "phone_number", 'user_level', 'is_authentication', 'authentication_image']
    

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=50, required=True, min_length=8)
    password2 = serializers.CharField(max_length=50, required=True)

    def validate(self, attrs):

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('password is not match', status.HTTP_400_BAD_REQUEST)

        return attrs


class CartBankModelSerializer(serializers.ModelSerializer):
    cart_number = serializers.CharField(max_length=16,min_length=16,required=True)

    class Meta:
        model = CartBankModel
        fields = ['cart_number']