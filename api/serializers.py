from enum import unique
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Item, Order, OrderDetails, Photo, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ['id', 'photo', 'item']


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class ItemPhotoSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)

    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_detail_items = serializers.ListField()
    class Meta:
        model = Order
        exclude = ['user', 'created', 'total']


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        exclude = ['user']


class OrderDetailsItemsSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    user = UserSerializer()

    class Meta:
        model = OrderDetails
        fields = '__all__'

class OrderUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    order_detail_items = OrderDetailsSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'


class GetOrderSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    order_detail_items = OrderDetailsSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'