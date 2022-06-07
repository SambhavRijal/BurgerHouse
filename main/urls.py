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
    path("cartdelete<int:id>/",views.cartdelete,name="cartdelete"),
    path("cartedit<int:id>/",views.cartedit,name="cartedit"),
    path("details/",views.details,name="details"),
    path("dashboard<int:id>/",views.dashboard,name="dashboard"),
    path("deleteorder<int:id>/",views.deleteorder,name="deleteorder"),
    path("changestate<int:id>st<int:state>/",views.changestate,name="changestate")
]