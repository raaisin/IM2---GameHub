from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing, name='landing'),  
    path('landing/', views.landing, name='landing'),  
    path('login/', views.login_view, name='login'),  
    path('signup/', views.signup_view, name='signup'),  
    path('home/', views.home_view, name='home'),
    path('carts/', views.cart_view, name='carts'),
    path('profile/', views.profile_view, name='profile'),
    path('laptop/', views.laptop_view, name='laptop'),
    path('phone/', views.phone_view, name='phone'),
    path('gamingphone/', views.gamingphone_view, name='gamingphone'),
    path('nongamingphone/', views.nongamingphone_view, name='nongamingphone'),
    path('new/', views.new_view, name='new'),
    path('deals/', views.deals_view, name='deals'),
    path('pc/', views.pc_view, name='pc'),
    path('active/', views.active_view, name='active'),
    path('accessories/', views.accessories_view, name='accessories'),
    path('orders/', views.orders, name='orders'),
    path('api/create-order/', views.create_order, name='create_order'),
        path('orders/<int:order_id>/mark-delivered/', views.mark_delivered, name='mark_delivered'),

]