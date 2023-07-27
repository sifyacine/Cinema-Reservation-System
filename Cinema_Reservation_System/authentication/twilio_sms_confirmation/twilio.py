from twilio.rest import Client
import twilio_settings
import random
from django.shortcuts import render, redirect
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required

@login_required
def send_verification_code(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if phone_number:
            # Generate a random verification code
            verification_code = str(random.randint(100000, 999999))

            # Save the verification code to the user's session
            request.session['verification_code'] = verification_code
            request.session.modified = True

            # Send the verification SMS using Twilio
            client = Client(twilio_settings.TWILIO_ACCOUNT_SID, twilio_settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f'Your verification code is: {verification_code}',
                from_=twilio_settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            # Save the verification code and the user's phone number in the database
            user = request.user
            user.phone_verification_code = verification_code
            user.phone_number = phone_number
            user.save()


            # Redirect the user to a verification page or show a form to enter the verification code
            return redirect('confirm_code.html')
        else:
            return render(request, 'phone_verification.html')
    else:
        return render(request, 'verify_code.html')



def confirm_verification_code(request):
    if request.method == 'POST':
        user = request.user
        verification_code = request.POST.get('verification_code')
        if user.phone_verification_code == verification_code:
            user.phone_verified = True
            user.save()
            return(request, 'phone_verified.html')
        else:
            return render(request, 'phone_verification_invalid.html')
    return render(request, 'phone_verification.html')