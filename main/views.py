from itertools import product
import string
from django.http.request import HttpRequest
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Item,Cart,Order,UserDetails 
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUser
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models import Q     

# Create your views here.

def index(request):
    if 'location' in request.session:
        print("test 1")
        if request.session['location'] !='':
            location=request.session['location']
            print("test 2"+location)
            return redirect("/rollback"+location)

    items=Item.objects.filter(featured=1)
    if request.user.is_active:
        print("User is active")
        person=UserDetails.objects.get(user=request.user)
        role=person.role
        id=request.user.id
        print("id of user is ", id)
        if role=="branch" or role=="delivery":
            return redirect("/dashboard"+str(id))

        if request.user.is_superuser==True:
            return redirect("/admin")

        existing_detail=UserDetails.objects.filter(user=request.user).count()
        if existing_detail==1:
            print("Details exist")
            return render(request,'main/index.html',{'items':items})
        else:
            print("Details doesnt exist"+str(existing_detail))
            return redirect("/details/") 
    else:
        return render(request,'main/index.html',{'items':items})

def menu(request):
    items=Item.objects.all()
    return render(request,'main/menu.html',{'items':items})


def food(request,id):
    item=Item.objects.get(id=id) 
    in_cart=0
    if request.user.is_authenticated:
        if Cart.objects.filter(user=request.user,product=item).count()==1:
            in_cart=Cart.objects.get(user=request.user,product=item)
            in_cart=in_cart.quantity
            print ("in cart",in_cart)
        else:
            in_cart=0
        return render(request,'main/food.html',{'item':item,'in_cart':in_cart})
    else:
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
    product=id
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
    
    message="Added to Cart"
    if request.user.is_active:
        message="Login Before Purchasing"
    
    items=Item.objects.all()
    return render(request,'main/menu.html',{'items':items,'message':message,'product':product})
    


def cartdelete(request,id):
    Cart.objects.filter(id=id).delete()
    return redirect("/cart/")


def cartedit(request,id):
    item=Cart.objects.get(id=id)

    if request.method=="POST":
        item.quantity=request.POST.get("quantity")
        print("Quantity=",item.quantity, "Price = ",item.price)
        item.total=int(item.price)*int(item.quantity)
        print("Total",item.total)
        item.save()
        return redirect("/cart/")
    else:
        return render(request,'main/cartedit.html',{'item':item})


# Purchase

def purchase(request,id):
    item=Item.objects.get(id=id)
    user=UserDetails.objects.get(user=request.user)
    province=user.province
    district=user.district
    town=user.town
    area=user.area
    order=Order.objects.create(user=request.user,product=item,quantity=1,price=item.price,total=item.price,province=province, district=district, town=town, area=area)
    order.save()

    return redirect("/confirmation/")

def checkout(request):
    cart_items=Cart.objects.filter(user=request.user)
    user=UserDetails.objects.get(user=request.user)
    province=user.province
    district=user.district
    town=user.town
    area=user.area

    for item in cart_items:
        order=Order.objects.create(user=request.user,product=item.product,quantity=item.quantity,price=item.price,total=item.total,province=province, district=district, town=town, area=area)
        order.save()
    cart_items.delete()
    return redirect("/confirmation/")


# User Register
def register(request):
    if request.method=="POST":
        form=RegisterUser(request.POST)
        if form.is_valid:
            form.save()
        return redirect("/")

    form=RegisterUser()
    return render(request,"main/register.html",{'form':form})


def details(request):
    if request.method=="POST":
        province=request.POST.get("province")
        district=request.POST.get("district")
        town=request.POST.get("town")
        area=request.POST.get("area")
        detail=UserDetails.objects.create(user=request.user,province=province,district=district,town=town,area=area)
        detail.save()
        return redirect("/")
    else:
        return render(request,'main/details.html')

# Dashboard
def dashboard(request,id):
    person=UserDetails.objects.get(user=request.user)
    role=person.role
    branch_town=UserDetails.objects.get(user=request.user)
    town=branch_town.town
    if role=="branch":
        #customers=UserDetails.objects.filter(town=town)
        orders=Order.objects.filter(Q(status='placed') | Q(status='confirmed'),town=town)
        history=Order.objects.filter(town=town,status="delivered")
        return render(request,"main/dashboard.html",{'orders':orders,'role':role,'history':history})

    elif role=="customer":
        orders=Order.objects.filter(Q(status='placed') | Q(status='confirmed') | Q(status='cooked') | Q(status='delivering'),user=request.user).order_by('-time')
        history=Order.objects.filter(user=request.user,status="delivered").order_by('-time')
        return render(request,"main/dashboard.html",{'orders':orders,'role':role,'history':history})

    elif role=="delivery":
        orders=Order.objects.filter(Q(status='cooked') | Q(status='delivering'),town=town)
        history=Order.objects.filter(status='delivered',town=town)
        return render(request,"main/dashboard.html",{'orders':orders,'role':role,'history':history})

    else:
        return redirect("/")
        

def deleteorder(request,id):
    Order.objects.get(id=id).delete()
    return redirect(dashboard,id=request.user.id)

def changestate(request,id,state):
    order=Order.objects.get(id=id)
    print("Inside changestate")
    print("State is",state)
    # state: 0=> placed   1=>confirmed   2=>cooked  3=>Delivering  4=>Delivered
    if state==1:
        order.status='confirmed'
    elif state==2:
        order.status='cooked'
    elif state==3:
        order.status='delivering'
    elif state==4:
        order.status='delivered'
    else:
        order.status='placed'
    order.save()
    return redirect(dashboard,id=request.user.id)

def confirmation(request):
    return render(request,"main/confirmation.html")

def rollback(request, id):
    if 'location' in request.session:
        location=request.session['location']
        if(location!=''):
            request.session['location']=''
            return redirect("/menu/food"+location)
    request.session['location'] = str(id)
    print("location is "+ request.session['location'] )
    return redirect("/login/")

