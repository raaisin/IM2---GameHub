from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    sold = models.IntegerField()
    colors = models.JSONField(default=list)
    image = models.ImageField(upload_to='images/')
    
    # Additional fields to capture more details
    specification_name = models.CharField(max_length=100, blank=True, null=True)
    specification_options = models.JSONField(default=list)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, default="")

    def __str__(self):
        return self.user.username
class CartItem(models.Model):
    """
    Cart item model that ensures user-specific cart functionality
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)

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
        ordering = ['-added_at']

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
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