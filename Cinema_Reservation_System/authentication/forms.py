from django import forms
from django.contrib.auth import authenticate
from .models import UserProfile

class SignUpForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']


from django import forms

class SignInForm(forms.Form):
    identifier = forms.CharField(label='Phone Number or Email')
    password = forms.CharField(widget=forms.PasswordInput)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email")