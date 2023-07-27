from rest_framework.generics import CreateAPIView
from .models import UserProfile
from .serializers import UserProfileSerializer, SignInSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import check_password

class UserProfileCreateView(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class SignInView(APIView):
    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            email_or_phone = serializer.validated_data['email_or_phone']
            password = serializer.validated_data['password']
            try:
                # Retrieve the user based on the provided email
                user_profile = UserProfile.objects.get(email=email_or_phone)
                if user_profile.email == email_or_phone or user_profile.phone_number == email_or_phone:
                    if user_profile.password == password:
                        return Response({"message": "access accepted."})  
                    else:
                        return Response({"message": "wrong password."})  
                else:
                    return Response({"message": "wrong email or phone number."})
                          
            except UserProfile.DoesNotExist:
                # User not found, return error response
                return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            # Invalid input data, return error response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
