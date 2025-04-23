# authentication/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserRegistration
from django.views.decorators.csrf import csrf_protect
import re

@csrf_protect
def user_login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to dashboard if already logged in

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        remember = request.POST.get('remember', False) == 'on'

        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return JsonResponse({'success': False, 'message': 'Invalid email format!', 'field': 'email'})

        # Authenticate user
        user = authenticate(request, username=email, password=password)  # Using email as username
        if user is None:
            # Check if email exists
            if not User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email not registered!', 'field': 'email'})
            return JsonResponse({'success': False, 'message': 'Incorrect password!', 'field': 'password'})

        # Login user
        login(request, user)
        
        # Handle "Remember Me"
        if not remember:
            request.session.set_expiry(0)  # Session expires when browser closes
        else:
            request.session.set_expiry(1209600)  # 2 weeks expiry for "Remember Me"

        return JsonResponse({'success': True, 'message': 'Login successful!'})

    return render(request, 'Public/Auth/UserLogin.html')

@csrf_protect
def user_register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        terms = request.POST.get('terms', False) == 'on'

        if not name or not email or not password:
            return JsonResponse({'success': False, 'message': 'All fields are required!'})

        if not re.match(r'^[A-Za-z\s]{2,}$', name):
            return JsonResponse({'success': False, 'message': 'Name must be at least 2 characters and contain only letters and spaces!'})

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return JsonResponse({'success': False, 'message': 'Invalid email format!'})

        valid_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'com.np']
        domain = email.split('@')[1].lower()
        if domain not in valid_domains:
            return JsonResponse({'success': False, 'message': 'Email domain must be gmail.com, yahoo.com, hotmail.com, outlook.com, or com.np!'})

        if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            return JsonResponse({'success': False, 'message': 'Password must be at least 8 characters long and contain at least one letter and one number!'})

        if not terms:
            return JsonResponse({'success': False, 'message': 'You must agree to the Terms of Use and Privacy Policy!'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Email already registered!'})

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )
            UserRegistration.objects.create(user=user)
            return JsonResponse({'success': True, 'message': 'Registration successful!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Registration failed: {str(e)}'})

    return render(request, 'Public/Auth/UserRegister.html')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'Public/Dashboards/Dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')