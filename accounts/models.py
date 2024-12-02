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
    name = models.CharField(max_length=255)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    rating = models.DecimalField(max_digits=3, decimal_places=1)  
    sold = models.IntegerField()  
    colors = models.JSONField(default=list)  
    image = models.ImageField(upload_to='phones/', null=True, blank=True) 

    def __str__(self):
        return self.name

    def image_tag(self):
        """Generate an HTML image tag for the phone image"""
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')
        return 'No Image'
    image_tag.short_description = 'Image'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_rating_stars(self):
        full_stars = int(self.rating)
        half_star = self.rating - full_stars >= 0.5
        return '★' * full_stars + ('½' if half_star else '')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, default="")

    def __str__(self):
        return self.user.username
class CartItem(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    color = models.CharField(max_length=20, default="no color")
    
    def __str__(self):
        return f"{self.product} ({self.quantity}) - {self.user.username}"

    @property
    def total_price(self):
        """
        Calculate the total price for this cart item.
        """
        return self.quantity * self.product.price  # Use product.price here

    class Meta:
        unique_together = ('user', 'product')


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
    products = models.TextField('Product', default="products")

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class PaymentMethod(models.Model): 
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    total = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f'Payment {self.id} for Order {self.order.id}'
    
class New(models.Model):
    name = models.CharField(max_length=255) 
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    rating = models.DecimalField(max_digits=3, decimal_places=1)  
    sold = models.IntegerField()  
    image = models.ImageField(upload_to='phones/', null=True, blank=True)  

    def __str__(self):
        return self.name

    def image_tag(self):
        """Generate an HTML image tag for the phone image"""
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')
        return 'No Image'
    image_tag.short_description = 'Image'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_rating_stars(self):
        """Convert numeric rating to star representation"""
        full_stars = int(self.rating)
        half_star = self.rating - full_stars >= 0.5
        return '★' * full_stars + ('½' if half_star else '')

from django.db import models

class Deal(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='deals/')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    sale_badge = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def get_rating_stars(self):
        """Convert numeric rating to star representation"""
        full_stars = int(self.rating)
        half_star = self.rating - full_stars >= 0.5
        return '★' * full_stars + ('½' if half_star else '')
    
class PC(models.Model):
    PRODUCT_BAGDE_CHOICES = [
        ('Best Seller', 'Best Seller'),
        ('New Arrival', 'New Arrival'),
        ('Best Value', 'Best Value'),
    ]

    name = models.CharField(max_length=255)
    badge = models.CharField(max_length=20, choices=PRODUCT_BAGDE_CHOICES)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    savings = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # Average rating
    review_count = models.IntegerField()

    # Product specifications
    gpu = models.CharField(max_length=255)
    cpu = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    storage = models.CharField(max_length=255)
    cooling = models.CharField(max_length=255)

    fps_1440p = models.DecimalField(max_digits=5, decimal_places=2)
    fps_4k = models.DecimalField(max_digits=5, decimal_places=2)
    ray_tracing = models.BooleanField(default=False)
    psu = models.CharField(max_length=255)

    # Images
    image_main = models.ImageField(upload_to='product_images/')

    case_lighting_choices = [
        ('RGB (MSI Mystic Light)', 'RGB (MSI Mystic Light)'),
        ('White LED', 'White LED'),
        ('No Lighting', 'No Lighting'),
    ]
    ram_configuration_choices = [
        ('32GB DDR5-6000 (2x16GB)', '32GB DDR5-6000 (2x16GB)'),
        ('64GB DDR5-6000 (4x16GB) (+$299)', '64GB DDR5-6000 (4x16GB) (+$299)'),
        ('128GB DDR5-6000 (4x32GB) (+$599)', '128GB DDR5-6000 (4x32GB) (+$599)'),
    ]
    warranty_choices = [
        ('2 Year Standard Warranty', '2 Year Standard Warranty'),
        ('3 Year Extended Warranty (+$199)', '3 Year Extended Warranty (+$199)'),
        ('4 Year Premium Warranty (+$299)', '4 Year Premium Warranty (+$299)'),
    ]

    case_lighting = models.CharField(max_length=50, choices=case_lighting_choices)
    ram_configuration = models.CharField(max_length=50, choices=ram_configuration_choices)
    warranty = models.CharField(max_length=50, choices=warranty_choices)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.name
class Accessory(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'{self.brand} {self.name}'

    class Meta:
        ordering = ['name']