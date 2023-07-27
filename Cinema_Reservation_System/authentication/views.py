from rest_framework.generics import CreateAPIView
from .models import UserProfile
from .serializers import UserProfileSerializer, SignInSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserProfileCreateView(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class SignInView(APIView):
    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            email_or_phone = serializer.validated_data['email_or_phone']
            password = serializer.validated_data['password']

            # Try to fetch user based on email
            try:
                user_profile = UserProfile.objects.get(email=email_or_phone)

                # Authenticate the user based on fetched user object
                user = authenticate(request, username=user_profile.email, password=password)

                if user is not None:
                    # User is authenticated, perform login and return success response
                    login(request, user)
                    return Response({"message": "User authenticated successfully."})

            except UserProfile.DoesNotExist:
                pass

            # User authentication failed, return error response
            return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Invalid input data, return error response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)