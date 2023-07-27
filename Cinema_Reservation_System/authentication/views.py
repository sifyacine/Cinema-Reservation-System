from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth import authenticate, login

def sign_in_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email_or_phone = form.cleaned_data['email_or_phone']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email_or_phone, password=password)

            if user is not None:
                login(request, user)
                return redirect('signup') 
            else:
                form.add_error(None, 'Invalid email/phone or password.')

    else:
        form = SignInForm()

    return render(request, 'signin.html', {'form': form})


def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            return redirect('signin')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

















# from rest_framework.generics import CreateAPIView
# from .models import UserProfile
# from .serializers import UserProfileSerializer, SignInSerializer
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status

# # signup views 
# class UserProfileCreateView(CreateAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
    
# # signin views
# class SignInView(APIView):
#     def post(self, request):
#         serializer = SignInSerializer(data=request.data)
#         if serializer.is_valid():
#             email_or_phone = serializer.validated_data['email_or_phone']
#             password = serializer.validated_data['password']

#             try:
#                 user_profile = UserProfile.objects.get(email=email_or_phone) 
#                 if user_profile.password == password:
#                     return Response({"message": "Access accepted."})
#                 else:
#                     return Response({"message": "Wrong password."})

#             except UserProfile.DoesNotExist:
#                 try:
#                     user_profile = UserProfile.objects.get(phone_number=email_or_phone)
#                     if user_profile.password == password:
#                         return Response({"message": "Access accepted."})
#                     else:
#                         return Response({"message": "Wrong password."})
                
#                 except UserProfile.DoesNotExist:
#                     return Response({"message": "Wrong email or phone number."}, status=status.HTTP_401_UNAUTHORIZED)

#         else:

#            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
