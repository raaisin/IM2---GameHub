from django.contrib import admin
from .models import Product, Order, OrderItem, CartItem, Profile, PaymentMethod

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Profile)
admin.site.register(PaymentMethod)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'user', 'date_ordered', 'status', 'total_amount']
    list_filter = ['status', 'date_ordered']
    search_fields = ['user__username', 'id']

admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)  






