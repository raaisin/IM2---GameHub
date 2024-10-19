from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import CartItem 
from django.contrib.auth.models import User
from django.contrib import messages


def landing(request):
    print("Landing page view called") 
    return render(request, 'landing.html')
 
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
    return render(request, 'login.html')
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        signup_method = request.POST.get('signup_method')

        if signup_method == 'gmail':
            # Handle Gmail sign-up
            first_name = request.POST.get('firstname', '').strip()
            last_name = request.POST.get('lastname', '').strip()
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            
            # Validate form data
            if not first_name or not last_name or not username or not email or not password:
                messages.error(request, "All fields are required for Gmail sign-up.")
                return render(request, 'signup.html')
            
            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken. Please choose another one.")
                return render(request, 'signup.html')
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return render(request, 'signup.html')
            
            # Check if email is a Gmail address
            if not email.endswith('@gmail.com'):
                messages.error(request, "Please use a valid Gmail address.")
                return render(request, 'signup.html')

            # Create a new user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            
            # Log the user in
            login(request, user)
            messages.success(request, "Account created successfully with Gmail!")
            return redirect('home')

        elif signup_method == 'facebook':
            # Placeholder for Facebook sign-up handling
            messages.info(request, "Facebook sign-up is not yet implemented.")
            return render(request, 'signup.html')
    
    return render(request, 'signup.html')


@login_required
def home_view(request):
    return render(request, 'home.html')

def cart_view(request):
    return render(request, 'cart.html')

@login_required
def profile_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'profile.html', context)

def laptop_view(request):
   
   return render(request, 'laptop.html')

def new_view(request):
    return render(request, 'new.html')
