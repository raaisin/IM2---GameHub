from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing, name='landing'),  
    path('landing/', views.landing, name='landing'),  
    path('login/', views.login_view, name='login'),  
    path('signup/', views.signup_view, name='signup'),  
    path('home/', views.home_view, name='home'),
    path('cart/', views.cart_view, name='cart'),
    path('profile/', views.profile_view, name='profile'),
]
