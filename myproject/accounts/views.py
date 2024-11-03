from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import CartItem 
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product

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
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('signup')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')
    return render(request, 'signup.html')



@login_required
def home_view(request):
    return render(request, 'home.html')

def cart_view(request):
    return render(request, 'carts.html')

@login_required
def profile_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'profile.html', context)

def laptop_view(request):
   
   return render(request, 'laptop.html')

def phone_view(request):
   
   return render(request, 'phone.html')

def new_view(request):
    return render(request, 'new.html')

def deals_view(request):
    return render(request, 'deals.html')

def pc_view(request):
    return render(request, 'pc.html')

def active_view(request):
    return render(request, 'active.html')

def accessories_view(request):
    return render(request, 'accessories.html')
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart') 

@login_required
def carts(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    tax = total_price * 0.08  # 8% tax
    grand_total = total_price + tax
    return render(request, 'carts.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'tax': tax,
        'grand_total': grand_total,
    })
def laptops(request):
    products = Product.objects.all()
    return render(request, 'laptops.html', {'products': products})

def orders(request):
    return render(request, 'orders.html')