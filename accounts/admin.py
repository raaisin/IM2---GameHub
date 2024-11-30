from django.contrib import admin
from .models import Product, Order, OrderItem, CartItem, Profile, PaymentMethod, Phone
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Profile)
admin.site.register(PaymentMethod)
admin.site.register(Phone)

class PhoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'sold', 'image_tag')  # Customize fields shown in the admin list
    search_fields = ('name', 'colors')  # Add search fields
    list_filter = ('sold', 'rating') 

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'user', 'date_ordered', 'status', 'total_amount']
    list_filter = ['status']
    search_fields = ['user__username', 'id']

admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)  