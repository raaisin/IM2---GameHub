from datetime import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    sold = models.IntegerField()
    colors = models.JSONField(default=list)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')
        return 'No Image'
    image_tag.short_description = 'Image'


class Phone(models.Model):
    name = models.CharField(max_length=255)  # Phone name
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Phone price
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # Phone rating
    sold = models.IntegerField()  # Number of phones sold
    colors = models.JSONField(default=list)  # List of available colors for the phone
    image = models.ImageField(upload_to='phones/', null=True, blank=True)  # Image of the phone

    def __str__(self):
        return self.name

    def image_tag(self):
        """Generate an HTML image tag for the phone image"""
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')
        return 'No Image'
    image_tag.short_description = 'Image'

    def save(self, *args, **kwargs):
        # You can add any pre-save or post-save operations if needed
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, default="")

    def __str__(self):
        return self.user.username
    
class CartItem(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.ForeignKey('Product', on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.product_name} ({self.quantity}) - {self.user.username}"

    @property
    def total_price(self):
        """
        Calculate the total price for this cart item
        """
        return self.quantity * self.price

    class Meta:
        # Ensure uniqueness of product per user to prevent duplicate entries
        unique_together = ('user', 'product_name')
        # ordering = ['-added_at']

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class PaymentMethod(models.Model):  # Fixed class name and made it a proper model
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Changed from PositiveBigIntegerField
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Fixed max_digits
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Fixed max_digits

    def __str__(self):
        return f'Payment {self.id} for Order {self.order.id}'