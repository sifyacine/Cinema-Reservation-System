from twilio.rest import Client
import twilio_settings
import random
from django.shortcuts import render
from django.contrib.sessions.backends.db import SessionStore


def send_confirmation_sms(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if phone_number:
            # Generate a random confirmation code
            confirmation_code = str(random.randint(100000, 999999))

            # Save the confirmation code to the user's session
            request.session['confirmation_code'] = confirmation_code
            request.session.modified = True

            # Send the confirmation SMS using Twilio
            client = Client(twilio_settings.TWILIO_ACCOUNT_SID, twilio_settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f'Your confirmation code is: {confirmation_code}',
                from_=twilio_settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )

            # Redirect the user to a confirmation page or show a form to enter the confirmation code
            return render(request, 'confirm_code.html')

    # Handle other form submission cases or show the registration form
    return render(request, 'signup.html')



def verify_confirmation_code(request):
    if request.method == 'POST':
        confirmation_code = request.POST.get('confirmation_code')

        # Retrieve the stored confirmation code from the user's session
        stored_code = 'get_the_stored_code_here'