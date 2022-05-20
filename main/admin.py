from django.contrib import admin
from .models import Item,Cart,Order

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','featured')

class CartAdmin(admin.ModelAdmin):
    list_display=('user','product','price','quantity','total')

class OrderAdmin(admin.ModelAdmin):
    list_display=('user','product','price','quantity','total','time')

admin.site.register(Item,ItemAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Order,OrderAdmin)