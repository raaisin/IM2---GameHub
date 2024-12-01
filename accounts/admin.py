from django.contrib import admin
from .models import Product, Order, OrderItem, CartItem, Profile, PaymentMethod, Phone, New, Deal, PC
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Profile)
admin.site.register(PaymentMethod)
admin.site.register(Phone)
admin.site.register(New)
admin.site.register(Deal)
admin.site.register(PC)

class PCAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'rating', 'product_type', 'category', 'created_at')
    search_fields = ('title', 'description', 'specs')
    list_filter = ('category', 'product_type', 'rating')
    ordering = ['-created_at']
    readonly_fields = ('created_at',) 

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'specs', 'price', 'discount_price', 'rating', 'product_type', 'category')
        }),
        ('Advanced Options', {
            'classes': ('collapse',),
            'fields': ('created_at',)
        }),
    )
class DealAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'discounted_price', 'rating', 'created_at')


class PhoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'sold', 'image_tag')  # Customize fields shown in the admin list
    search_fields = ('name', 'colors')  # Add search fields
    list_filter = ('sold', 'rating') 

class NewAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'sold', 'image_tag')  # Customize fields shown in the admin list
    search_fields = ('name')  # Add search fields
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