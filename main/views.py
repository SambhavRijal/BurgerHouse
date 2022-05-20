from itertools import product
from django.http.request import HttpRequest
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Item,Cart, Order
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUser
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your views here.

def index(request):
    items=Item.objects.filter(featured=1)
    return render(request,'main/index.html',{'items':items})

def menu(request):
    items=Item.objects.all()
    return render(request,'main/menu.html',{'items':items})

def food(request,id):
    item=Item.objects.get(id=id)
    return render(request,'main/food.html',{'item':item})


# Cart System
def cart(request):
    total=0
    cart_items=Cart.objects.filter(user=request.user)
    for item in cart_items:
        total=total+item.total
        print(total)
    return render(request,'main/cart.html',{'items':cart_items,'total':total})

def addtocart(request,id):
    count=Cart.objects.filter(product=Item.objects.get(id=id),user=request.user).count()
    print("Count=",count)
    if count==1:
        i=Cart.objects.get(product=Item.objects.get(id=id),user=request.user)
        q=i.quantity
        q=q+1
        i.quantity=q
        i.total=i.price*i.quantity
        i.save()
    else:
        c=Cart.objects.create(user=request.user,product=Item.objects.get(id=id),price=Item.objects.only('price').get(id=id).price,total=Item.objects.only('price').get(id=id).price)
        c.save()
        print("New Entry added")
    return redirect("/menu/")


# Purchase
def checkout(request):
    cart_items=Cart.objects.filter(user=request.user)
    for item in cart_items:
        order=Order.objects.create(user=request.user,product=item.product,quantity=item.quantity,price=item.price,total=item.total)
        order.save()
    cart_items.delete()
    return redirect("/")

# User Register
def register(request):
    if request.method=="POST":
        form=RegisterUser(request.POST)
        if form.is_valid:
            form.save()
        return redirect("/")

    form=RegisterUser()
    return render(request,"main/register.html",{'form':form})