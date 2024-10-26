from django.db import models
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "Product Categories"

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    #category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.product.product_name} ({self.quantity})'
    
    @property
    def total_price(self):
        return self.quantity * self.product.price

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
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.product.product_name} in Order {self.order.id}'
    
class payment_method:
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    price = models.DecimalField(max_digits=0, decimal_places=2)
    total = models.DecimalField(max_digits=0, decimal_places=2)

    def __str__(self):
        return f'{self.id} in Order {self.order.id}' 