from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("menu/",views.menu,name="menu"),
    path("menu/food<int:id>/",views.food,name="food"),
    path("register/",views.register,name="register"),
    path("cart/",views.cart,name="cart"),
    path("addtocart<int:id>/",views.addtocart,name="addtocart"),
    path("checkout/",views.checkout,name="checkout"),
]