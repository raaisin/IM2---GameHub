from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import CartItem, Deal, New 
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist
from .models import Order, OrderItem, Product, Phone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

from accounts import models

def landing(request):
    print("Landing page view called") 
    return render(request, 'features/landing.html')
 
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        login_type = request.POST.get('login_type', 'user')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if login_type == 'admin' and user.is_staff:
                login(request, user)
                return redirect('dashboard')  
            elif login_type == 'user' and not user.is_staff:
                login(request, user)
                return redirect('home') 
            else:
                return render(request, 'user/login.html', {'error': 'Unauthorized access'})
        
        return render(request, 'user/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'user/login.html')
@login_required
def dashboard_view(request):
    return render(request, 'features/dashboard.html')

def dashboard(request):
    recent_orders = Order.objects.all().order_by('-order_date')[:10]  
    
    context = {
        'recent_orders': recent_orders,
        'total_sales': calculate_total_sales(), # type: ignore
        'total_orders': Order.objects.count(),
        'total_products': Product.objects.count(),
        'total_customers': Customer.objects.count() # type: ignore
    }
    
    return render(request, 'features/dashboard.html', context)



def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signup')

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
    return render(request, 'user/signup.html')



@login_required
def home_view(request):
    return render(request, 'features/home.html')

@login_required
def cart_view(request):
    if request.method == 'GET':
        cart_items = CartItem.objects.filter(user=request.user)
        return render(request, 'features/carts.html', {'cart_items': cart_items})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_name = data.get('product_name')
            quantity = data.get('quantity', 1)
            price = data.get('price', 0.0)

            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product_name=product_name,
                defaults={'quantity': quantity, 'price': price}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return JsonResponse({'success': True, 'message': 'Item added to cart!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

@login_required
def profile_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            if User.objects.filter(username=data.get('username')).exclude(id=request.user.id).exists():
                return JsonResponse({"success": False, "error": "Username already exists."})
            
            if User.objects.filter(email=data.get('email')).exclude(id=request.user.id).exists():
                return JsonResponse({"success": False, "error": "Email already exists."})

            request.user.username = data.get('username', request.user.username)
            request.user.email = data.get('email', request.user.email)
            request.user.save()

            Profile.objects.update_or_create(
                user=request.user,
                defaults={'bio': data.get('bio', '')}
            )

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return render(request, 'user/profile.html', {'user': request.user})

def laptop_view(request):
    products = Product.objects.all()
    for product in products:
        if product.image:
            print(f"Product: {product.name}")
            print(f"Image URL: {product.image.url}")
            print(f"Image Path: {product.image.path}")
            print(f"Image exists: {os.path.exists(product.image.path)}")
        else:
            print(f"Product {product.name} has no image")
    return render(request, 'items/laptop.html', {'products': products})

def phone_view(request):
    phones = Phone.objects.all()
    
    for phone in phones:
        if phone.image:
            print(f"Product: {phone.name}")
            print(f"Image URL: {phone.image.url}")
            print(f"Image Path: {phone.image.path}")
            print(f"Image exists: {os.path.exists(phone.image.path)}")
        else:
            print(f"Product {phone.name} has no image")
    
    return render(request, 'items/phone.html', {'phones': phones})


def gamingphone_view(request):
   
   return render(request, 'items/gamingphone.html')

def new_view(request):
    items = New.objects.all()
    return render(request, 'items/new.html', {'items': items})

def deals_view(request):
    deals = Deal.objects.all()
    return render(request, 'items/deals.html', {'deals': deals})


from django.shortcuts import render
from .models import PC

def pc_view(request):
    products = PC.objects.all()  # Query all the PC products from the database
    return render(request, 'items/pc.html', {'products': products})


def active_view(request):
    return render(request, 'items/active.html')

def accessories_view(request):
    return render(request, 'items/accessories.html')

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
    return render(request, 'features/carts.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'tax': tax,
        'grand_total': grand_total,
    })
def laptops(request):
    products = Product.objects.all()
    return render(request, 'laptops.html', {'products': products})

@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'features/orders.html', {'orders': user_orders})

@login_required
def dashboard(request):
    total_sales = Order.objects.filter(status='DELIVERED').aggregate(total=models.Sum('total_amount'))['total'] or 0
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_customers = User.objects.count()
    
    recent_orders = Order.objects.filter(status__in=['PENDING', 'PROCESSING']).order_by('-date_ordered')[:10]
    
    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_customers': total_customers,
        'orders': recent_orders
    }
    return render(request, 'admin_dashboard.html', {'user': request.user})

@require_POST
@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    new_status = request.POST.get('status')
    
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
        
        total_sales = Order.objects.filter(status='DELIVERED').aggregate(total=models.Sum('total_amount'))['total'] or 0
        
        return JsonResponse({
            'status': 'success', 
            'message': f'Order {order_id} status updated to {new_status}',
            'total_sales': float(total_sales)
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)
@require_POST
@login_required
def mark_all_orders_delivered(request):
    Order.objects.filter(status__in=['PENDING', 'PROCESSING']).update(status='DELIVERED')
    total_sales = Order.objects.filter(status='DELIVERED').aggregate(total=models.Sum('total_amount'))['total'] or 0

    return JsonResponse({
        'status': 'success',
        'message': 'All orders are delivered',
        'total_sales': float(total_sales)
     
    })
@require_POST
@login_required
def mark_all_orders_delivered(request):
    Order.objects.filter(status__in=['PENDING', 'PROCESSING']).update(status='DELIVERED')
    total_sales = Order.objects.filter(status='DELIVERED').aggregate(total=models.Sum('total_amount'))['total'] or 0
    
    return JsonResponse({
        'status': 'success', 
        'message': 'All orders marked as delivered',
        'total_sales': float(total_sales)
    })

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
        
        total_amount = sum(
            Decimal(str(item['price'])) * int(item['quantity'])
            for item in cart_items
        )
        
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            status='PENDING'
        )
        
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
    return render(request, 'features/payment.html')

def noitemsfound(request):
    return render(request, 'features/noitemsfound.html')

