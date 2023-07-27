from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'password')



class SignInSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password = serializers.CharField()

