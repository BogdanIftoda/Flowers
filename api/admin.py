from django.contrib import admin

from .models import Item, Order, OrderDetails, Photo, User
from rest_framework_simplejwt.models import TokenUser

# Register your models here.
admin.site.register(TokenUser)
admin.site.register(User)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Photo)
admin.site.register(OrderDetails)
