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

@login_required
def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            # Generate a verification token
            verification_token = str(uuid.uuid4())
            user.email_verification_token = verification_token
            
            user.save()

            # Send the verification email
            subject = 'Email Verification'
            message = f'Click the link below to verify your email:\n\n' \
                      f'http://example.com/verify_email/{verification_token}/'
            from_email = 'noreply@gmail.com'
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

            return redirect('email_verification_pending')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def email_verification_pending(request):
    return render(request, 'email_verification_pending.html')



def verify_email(request, verifiction_token):
    try:
        user = UserProfile.objects.get(email_verified=False)
        if user.email_verification_token == verifiction_token:
            user.email_verified = True
            user.save()
            return render(request, 'email_verified.html')
        else:
            return render(request, 'email_verification_invalid.html')
    
    except UserProfile.DoesNotExist:
        return render(request, 'email_verification_invalid.html')














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
