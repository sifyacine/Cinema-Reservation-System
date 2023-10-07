from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email")



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'  # Include all fields from the UserProfile model
