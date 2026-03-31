from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
import random
import time
from django.conf import settings

def user_login(request):
    context = {}
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        pw = request.POST.get('password')
        user = authenticate(request, username=user_name, password=pw)

        if user is not None:
            login(request, user)
            return redirect('home')

        context = {'error': 'Sorry username and password do not match'}

    return render(request, 'login.html', context)


# 🔥 UPDATED SIGNIN WITH OTP
def signin(request):
    context = {}

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2')
        em = request.POST.get('email')

        # 🔴 Password check
        if pw1 != pw2:
            context['error'] = "Passwords do not match"
            return render(request, 'signup.html', context)

        # 🔴 Username check
        if User.objects.filter(username=user_name).exists():
            context['error'] = "Username already exists"
            return render(request, 'signup.html', context)

        # 🔴 Email check (🔥 moved here correctly)
        if User.objects.filter(email=em).exists():
            context['error'] = "Email already registered"
            return render(request, 'signup.html', context)

        # 🔥 Generate OTP
        otp = str(random.randint(100000, 999999))

        # Save data in session
        request.session['otp'] = otp
        request.session['username'] = user_name
        request.session['password'] = pw1
        request.session['email'] = em

        # 🔥 Send Email
        try:
            send_mail(
                'Email Verification',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [em],
                fail_silently=False,
            )
        except Exception as e:
            context['error'] = f"Failed to send OTP: {str(e)}"
            return render(request, 'signup.html', context)

        return redirect('verify_otp')

    return render(request, 'signup.html', context)
# 🔥 OTP VERIFY VIEW
def verify_otp(request):
    context = {}
    
    # Check if OTP session exists
    if not request.session.get('otp'):
        return redirect('signin')
    
    # Initialize attempt count if not exists
    if 'otp_attempts' not in request.session:
        request.session['otp_attempts'] = 0
        request.session['otp_start_time'] = str(time.time())
    
    # Check if attempts exceeded
    if request.session['otp_attempts'] >= 3:
        context['error'] = "Maximum attempts exceeded. Please signup again."
        request.session.flush()
        return render(request, 'verify_otp.html', context)
    
    # Check timeout (2 minutes from last attempt)
    start_time = float(request.session.get('otp_start_time', time.time()))
    current_time = time.time()
    if current_time - start_time > 120:  # 2 minutes
        context['error'] = "OTP expired. Please signup again."
        request.session.flush()
        return render(request, 'verify_otp.html', context)
    
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        
        if user_otp == session_otp:
            # create user after verification
            User.objects.create_user(
                username=request.session.get('username'),
                password=request.session.get('password'),
                email=request.session.get('email')
            )
            
            # clear session
            request.session.flush()
            
            return redirect('login')
        else:
            # Increment attempts and refresh timeout
            request.session['otp_attempts'] += 1
            request.session['otp_start_time'] = str(time.time())
            
            remaining_attempts = 3 - request.session['otp_attempts']
            context['error'] = f"Invalid OTP. {remaining_attempts} attempts remaining."
            context['attempts_left'] = remaining_attempts
    
    return render(request, 'verify_otp.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')