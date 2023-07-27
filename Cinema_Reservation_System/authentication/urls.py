from django.urls import path
from .views import sign_in_view, sign_up_view, verify_email, email_verification_pending, email_verification_view

urlpatterns = [
    path('signup/', sign_up_view, name='signup'),
    path('signin/', sign_in_view, name='signin'),
    path('verify_email/<str:verification_token>/', verify_email, name='verify_email'),
    path('verification_code_entry/', email_verification_view, name='verification_code_entry'),
    path('email_verification_pending/', email_verification_pending, name='email_verification_pending'), 
]
