from django.db import models
from django.contrib.auth.models import AbstractUser


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
        return self.username


class Item(models.Model):

    FLOWER = 'FLOWER'
    NOTFLOWER = 'NOTFLOWER'

    TYPES = (
        (FLOWER, 'Flower'),
        (NOTFLOWER, 'NotFlower'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    in_stock = models.PositiveIntegerField(default=0)
    price = models.FloatField()
    item_type = models.CharField(
        max_length=50, choices=TYPES)

    def __str__(self):
        return self.name + ' ' + str(self.id)


class Photo(models.Model):

    FLOWER = 'flower'
    NOTFLOWER = 'notflower'

    TYPES = (
        (FLOWER, 'flower'),
        (FLOWER, 'notflower'),
    )

    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(
        upload_to='images/', blank=True, null=True)
    photo_type = models.CharField(max_length=60, choices=TYPES)

    def __str__(self):
        return self.item.name


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    order_competed = models.DateField()

    def __str__(self):
        return self.user.username + ' ' + str(self.order_date)


class BoquetInfo(models.Model):
    id = models.AutoField(primary_key=True)
    delivery_address = models.CharField(max_length=150)

    def __str__(self):
        return self.delivery_address


class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    boquet_info = models.ForeignKey(BoquetInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name
