from django.contrib import admin

from .models import Item, Order, OrderDetails, Photo, User

# Register your models here.

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Photo)
admin.site.register(OrderDetails)
