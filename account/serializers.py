from rest_framework import serializers
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'user_level', 'is_authentication']
    


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=50, required=True)
    password2 = serializers.CharField(max_length=50, required=True)

    def validate(self, attrs):

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('password is not match', status.HTTP_400_BAD_REQUEST)

        return attrs