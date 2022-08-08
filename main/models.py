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
    image = models.ImageField(upload_to='images/',default='images/uwp540709.jpeg')

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
    province=models.IntegerField(default=3)
    district=models.CharField(max_length=200,default='bhaktapur')
    town=models.CharField(max_length=200,default='thimi')
    area=models.CharField(max_length=200,default='main road')
    status=models.CharField(max_length=50,default='placed')


class UserDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=20,default='customer')
    province=models.IntegerField(default=3)
    district=models.CharField(max_length=200,default='Bhaktapur')
    town=models.CharField(max_length=200,default='Thimi')
    area=models.CharField(max_length=200,default='main road')

