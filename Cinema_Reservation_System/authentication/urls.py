from django.urls import path
from .views import sign_in_view, sign_up_view, confirm_verification_code

urlpatterns = [
    path('signup/', sign_up_view, name='signup'),
    path('signin/', sign_in_view, name='signin'),
    path('verify_phonenumber/',confirm_verification_code , name='confirm_verification'),
]
