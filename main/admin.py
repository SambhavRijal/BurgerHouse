from django.contrib import admin
from .models import Item,Cart,Order, UserDetails

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','featured','image')

class CartAdmin(admin.ModelAdmin):
    list_display=('user','product','price','quantity','total')

class OrderAdmin(admin.ModelAdmin):
    list_display=('user','product','price','quantity','total','time')

class UserDetailsAdmin(admin.ModelAdmin):
    list_display=('user','role','province','district','town','area')

admin.site.register(Item,ItemAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(UserDetails,UserDetailsAdmin)