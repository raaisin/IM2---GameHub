from django.db import models
from django.contrib.auth.models import User

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



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the User model
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product_name} ({self.quantity})'


class product_category(models.Model):
    category_name = models.CharField(max_length=100)

    def category_stuff(self):
        return self.category_name
    
#class Profile(models.Model):
  #  user = models.OneToOneField(User, on_delete=models.CASCADE)
  #  bio = models.TextField(blank=True)

   # def __str__(self):
      #  return self.user.username