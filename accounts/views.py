from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import CartItem 
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist
from .models import Order, OrderItem, Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal

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

# views.py
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def profile_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Update user fields
            request.user.username = data.get('username', request.user.username)
            request.user.email = data.get('email', request.user.email)
            request.user.save()

            # Update profile fields if you have a Profile model
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.bio = data. get('bio', profile.bio)  
            profile.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    # If the request is a GET, render the profile page
    return render(request, 'profile.html', {'user': request.user})

def laptop_view(request):
   
   return render(request, 'laptop.html')

def phone_view(request):
   
   return render(request, 'phone.html')

def gamingphone_view(request):
   
   return render(request, 'gamingphone.html')

def nongamingphone_view(request):
   
   return render(request, 'nongamingphone.html')

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

def lol_game(request):
    return render(request, 'games/lol.html')

def fortnite_game(request):
    return render(request, 'games/fortnite.html')

def valorant_game(request):
    return render(request, 'games/valorant.html')

def apex_game(request):
    return render(request, 'games/apex.html')

def csgo_game(request):
    return render(request, 'games/csgo.html')

def cyberpunk_game(request):
    return render(request, 'games/cyberpunk.html')

def eldenring_game(request):
    return render(request, 'games/eldenring.html')


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

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from django.http import HttpResponseForbidden

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'orders.html', {'orders': orders})

@login_required
def mark_delivered(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        
        # Ensure the user owns this order
        if order.user != request.user:
            return HttpResponseForbidden()
            
        order.delivered = True
        order.save()
        
        return redirect('orders')
    return redirect('orders')

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from decimal import Decimal
import json
from .models import Order, OrderItem, Product

@csrf_protect
@require_http_methods(["POST"])
def create_order(request):
    """Handle order creation from cart checkout"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Please log in to place an order'}, status=401)
    
    try:
        data = json.loads(request.body)
        cart_items = data.get('items', [])
        
        if not cart_items:
            return JsonResponse({'error': 'Cart is empty'}, status=400)
        
        # Calculate total amount
        total_amount = sum(
            Decimal(str(item['price'])) * int(item['quantity'])
            for item in cart_items
        )
        
        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            status='PENDING'
        )
        
        # Create order items
        for item in cart_items:
            try:
                product = Product.objects.get(name=item['name'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=Decimal(str(item['price']))
                )
            except Product.DoesNotExist:
                # If product doesn't exist, delete the order and return error
                order.delete()
                return JsonResponse({
                    'error': f'Product not found: {item["name"]}'
                }, status=400)
        
        return JsonResponse({
            'message': 'Order created successfully',
            'orderId': order.id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def payment_view(request):
    return render(request, 'payment.html')