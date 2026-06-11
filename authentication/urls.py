from django.urls import path

from .views import(
    UserRegistrationview, UserLoginView
)

from .views import send_otp_mail, verify_otp, set_new_password

urlpatterns = [
    path('register/', UserRegistrationview.as_view(), name = 'signup'),
    path('login/', UserLoginView.as_view(), name = 'signin'),

      # pwd reset
    path('send-otp/', send_otp_mail, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('set-new-password/', set_new_password, name='set_new_password'),



]