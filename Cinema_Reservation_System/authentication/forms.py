from django import forms
from .models import UserProfile

class SignUpForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']


from django import forms

class SignInForm(forms.Form):
    email_or_phone = forms.CharField(label='Email or Phone', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
