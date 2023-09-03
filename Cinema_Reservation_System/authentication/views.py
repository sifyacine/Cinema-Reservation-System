from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import SignUpForm, SignInForm
from twilio.rest import Client
import pyotp

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
            # Create a user profile
            user_profile = UserProfile.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password'],  # Hash the password in production
                phone_verified=False,
                email_verified=False,
            )

            # Generate and send verification code
            verification_code = generate_verification_code()
            send_verification_code(user_profile.phone_number, verification_code)

            # Store verification code and phone number in session
            request.session['verification_code'] = verification_code
            request.session['phone_number'] = user_profile.phone_number

            return redirect('confirm_verification')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

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
                return render(request, 'phone_verification_invalid.html')

            # Verify phone number
            user_profile.phone_verified = True
            user_profile.save()

            # Log the user in
            user = authenticate(request, username=user_profile.email, password=user_profile.password)

            if user is not None:
                login(request, user)
                return redirect('profile')  # Redirect to the user's profile page

    return render(request, 'confirm_verification.html')
