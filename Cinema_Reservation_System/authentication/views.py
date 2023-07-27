from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import uuid
from .models import UserProfile
from django.core.mail import send_mail




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
            # Save the user object after setting the password
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            # Generate a verification token
            verification_token = str(uuid.uuid4())
            user.email_verification_token = verification_token

            user.save()

            # Send the verification email
            subject = 'Email Verification'
            message = f'Click the link below to verify your email:\n\n' \
                      f'http://127.0.0.1:8000/verify_email/{verification_token}/'
            from_email = 'ycn585@gmail.com'  # Change this to your sending email address
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

            return redirect('verification_code_entry')  # Redirect to the verification code entry page

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def email_verification_pending(request):
    return render(request, 'email_verification_pending.html')

def verify_email(request, verification_token):
    try:
        user = UserProfile.objects.get(email_verification_token=verification_token)
        if user.email_verified:
            return render(request, 'email_verified.html')
        else:
            return redirect('verification_code_entry')
    except UserProfile.DoesNotExist:
        return render(request, 'email_verification_invalid.html')

def email_verification_view(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        try:
            user = UserProfile.objects.get(email_verification_token=verification_code)
            user.email_verified = True
            user.email_verification_token = None
            user.save()
            return render(request, 'email_verified.html')
        except UserProfile.DoesNotExist:
            return render(request, 'email_verification_invalid.html')

    return render(request, 'email_verification_entry.html')

















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
