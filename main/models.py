from datetime import datetime
from email.policy import default
from itertools import product
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    name=models.CharField(max_length=200)
    price=models.IntegerField()
    category=models.CharField(max_length=200,default='snacks')
    description=models.CharField(max_length=500,default='Tasty Food')
    featured=models.BooleanField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField(default=0)
    total=models.IntegerField(default=0)

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField(default=0)
    total=models.IntegerField(default=0)
    time=models.DateTimeField(auto_now_add=True)

