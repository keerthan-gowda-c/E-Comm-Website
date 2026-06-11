from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView

from django.views.generic import CreateView

from .forms import UserRegistrationForm, UserLoginForm



class UserRegistrationview(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'authentication/register.html'
    success_url = '/'


class UserLoginView(LoginView):
    template_name = 'authentication/login.html'
    authentication_form = UserLoginForm



# Email otp workflow for resetting  password

from .models import EmailOTP, OTP_EXPIRY_IN_MINUTES

import random as rn
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return str(rn.randint(100000, 999999))

def send_otp_mail (request):
    context = None
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            otp = generate_otp()
            EmailOTP.objects.create(email = email, otp = otp)

            # Prepare the email
            subject = "Your OTP Code"
            message = f"Your OTP is {otp}. It will expire in {OTP_EXPIRY_IN_MINUTES} minutes"
            send_mail(
                subject = subject,
                message = message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list = [email],
                fail_silently=False
            )

            request.session['email_for_reset'] = email 
            return redirect('verify_otp')
        context = {
            'error' : "Email missing"
        }
    if not context:
        context = {}

    return render(request, 
                      template_name='authentication/pwd_reset/send_otp_email.html', 
                      context=context)

# verifying the otp unless expired.

from django.contrib.auth.models import User
from .models import EmailOTP

def verify_otp(request):
    context = {}
    email = request.session.get('email_for_reset')

    if not email:
        return redirect('send_otp')  # safeguard

    if request.method == 'POST':
        otp_input = request.POST.get('otp')

        try:
            otp_record = EmailOTP.objects.filter(email=email, otp=otp_input).latest('created_at')
            if otp_record.is_expired():
                context['error'] = "OTP expired. Try again."
            else:
                # OTP is valid → redirect to password reset form with user info in session
                request.session['verified_email'] = email
                return redirect('set_new_password')
        except EmailOTP.DoesNotExist:
            context['error'] = "Invalid OTP. Try again."

    return render(request, 'authentication/pwd_reset/verify_otp.html', context)

# setting new password taking the verified email from session

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
def set_new_password(request):
    email = request.session.get('verified_email')
    if not email:
        return redirect('send_otp')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            # Clean session
            request.session.pop('verified_email', None)
            request.session.pop('email_for_reset', None)
            return render(request, 'authentication/pwd_reset/done.html')
    else:
        form = SetPasswordForm(user)
        context = {'form': form}

    return render(request=request, 
                  template_name='authentication/pwd_reset/set_new_password.html',
                  context=context )