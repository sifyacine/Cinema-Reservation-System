from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import UserProfile
from twilio.rest import Client
import pyotp
from .forms import SignInForm, SignUpForm  # Import your custom SignInForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import bcrypt



from django.contrib import auth

def sign_in_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password_written = form.cleaned_data['password']

            # Check if identifier is a phone number or an email
            if '@' in identifier:
                # Sign in with email
                try:
                    user_profile = UserProfile.objects.get(email=identifier)
                except UserProfile.DoesNotExist:
                    error_message = 'Invalid email or password'
                    return render(request, 'authentication/signin.html', {'form': form, 'error_message': error_message})
            else:
                # Sign in with phone number
                try:
                    user_profile = UserProfile.objects.get(phone_number=identifier)
                except UserProfile.DoesNotExist:
                    error_message = 'Invalid phone number or password'
                    return render(request, 'authentication/signin.html', {'form': form, 'error_message': error_message})

            # Use your custom authentication function
            is_authenticated = UserProfile(user_profile, password_written)

            if is_authenticated:
                # Log in the user manually (since we're not using Django's default authentication)
                request.session['user_id'] = user_profile.id  # Store user's ID in the session
                return redirect('home')
            else:
                error_message = 'Authentication failed'
                return render(request, 'authentication/signin.html', {'form': form, 'error_message': error_message})
    else:
        form = SignInForm()
    
    return render(request, 'authentication/signin.html', {'form': form})




# Function to generate a verification code
def generate_verification_code():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    verification_code = totp.now()
    return verification_code

# Function to send the verification code via SMS
def send_verification_code(phone_number, verification_code):
    # Use your Twilio account SID and auth token here
    account_sid = 'AC7894b22d75be7b2e0c08f24ee0fa42d0'
    auth_token = '9fb77427bd08448a4e0b94a00dcf8389'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+15736373763',
        body=f'Your verification code is: {verification_code}',
        to=phone_number
    )

    print(message.sid)



def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Hash the password
            password = form.cleaned_data['password']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Create a user profile
            user_profile = UserProfile.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                password=hashed_password.decode('utf-8'),  # Store the hashed password
                phone_verified=False,
                email_verified=False,
            )

            # Generate and send verification code
            verification_code = generate_verification_code()
            send_verification_code(user_profile.phone_number, verification_code)

            # Store verification code and phone number in session
            request.session['verification_code'] = verification_code
            request.session['phone_number'] = user_profile.phone_number

            return redirect('phone_verification/confirm_verification')
    else:
        form = SignUpForm()

    return render(request, 'authentication/signup.html', {'form': form})

def confirm_verification_code(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        stored_code = request.session.get('verification_code')

        if verification_code == stored_code:
            # Get phone number from session
            phone_number = request.session.get('phone_number')

            try:
                # Query user profile by phone number
                user_profile = UserProfile.objects.get(phone_number=phone_number)
            except UserProfile.DoesNotExist:
                return render(request, 'phone_verification/phone_verification_invalid.html')

            # Verify phone number
            user_profile.phone_verified = True
            user_profile.save()

            # Log the user in
            user = authenticate(request, username=user_profile.email, password=user_profile.password)

            if user is not None:
                login(request, user)
                return redirect('signin')  # Redirect to the user's profile page

    return render(request, 'phone_verification/confirm_verification.html')



User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email_written = request.POST['email']
        try:
            user = UserProfile.objects.get(email=email_written)
            reset_password_link = f'http://127.0.0.1:8000/registering/reset-password/{email_written}/'

            # Send an email with the reset password link
            subject = 'Password Reset Request'
            message = f'Please click the following link to reset your password:\n{reset_password_link}'
            from_email = 'ycn585@email.com'  # Replace with your email address
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return render(request, 'forget_passsword/forgot_password_email.html')
        except UserProfile.DoesNotExist:
            return render(request, 'forget_password/email_not_found.html')
    else:
        return render(request, 'forget_password/forgot_password_email.html')




def reset_password(request, email):
    try:
        user = UserProfile.objects.get(email=email)

        if request.method == 'POST':
            new_password = request.POST['new_password']

            # Update the user's password
            user.password = new_password
            user.save()

            return render(request, 'forget_password/password_reset_success.html')
        else:
            return render(request, 'forget_password/forgot_password_renew.html', {'email': email})
    except UserProfile.DoesNotExist:
        # Handle the case where the email doesn't exist
        return render(request, 'forget_password/email_not_found.html')






@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Important: Update the session to avoid automatic logout
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been successfully changed.')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})



@login_required  # Make sure the user is logged in to access this view
def user_profile(request):
    user = UserProfile.email
    try:
        profile = UserProfile.objects.get(email= user)
    except UserProfile.DoesNotExist:
        # Handle the case where the user profile doesn't exist
        profile = None

    if request.method == 'POST':
        # Handle form submission and update user profile
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']

        if profile is not None:
            # Update the user's profile if it exists
            profile.first_name = first_name
            profile.last_name = last_name
            profile.email = email
            profile.phone_number = phone_number
            profile.save()

    return render(request, 'profile/user_profile.html', {'profile': profile})




