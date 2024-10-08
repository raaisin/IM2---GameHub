from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    quantity = models.IntegerField()  
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

class cart_items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

class product_category(models.Model):
    category_name = models.CharField(max_length=100)

    def category_stuff(self):
        return self.category_name
    
