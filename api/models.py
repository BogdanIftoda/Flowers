from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.db.models.fields.related import ManyToManyField


class User(AbstractUser):

    ADMIN = 'admin'
    NOTADMIN = 'notadmin'

    ROLES = (
        (ADMIN, 'Admin'),
        (NOTADMIN, 'Notadmin'),
    )
    role = models.CharField(
        max_length=50, choices=ROLES, default=NOTADMIN)
    phone = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"{self.username}, {self.id}"


class Item(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    in_stock = models.PositiveIntegerField(default=0)
    price = models.FloatField()

    def __str__(self):
        return self.name + ' ' + str(self.id)


class Photo(models.Model):

    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='photos')
    photo = CloudinaryField('image')

    def __str__(self):
        return self.item.name

class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.item.name

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_detail_items = ManyToManyField(OrderDetails)
    delivery_address = models.CharField(max_length=150)
    order_date = models.DateField(auto_now_add=True)
    created = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ' ' + str(self.order_date)

    def get_order_total(self):
        total = 0
        for item in self.order_detail_items.all():
            total += item.get_product_total()
        return total