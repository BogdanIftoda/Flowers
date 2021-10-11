from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import BoquetInfo, Item, Order, OrderDetails, Photo, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

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
        fields = ['id', 'photo', 'photo_type', 'item']


class ItemSerializer(serializers.ModelSerializer):

    photos = PhotoSerializer(many=True)

    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Order
        fields = '__all__'


class BoquetInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoquetInfo
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):

    item = ItemSerializer()
    order = OrderSerializer()
    boquet_info = BoquetInfoSerializer()

    class Meta:
        model = OrderDetails
        fields = '__all__'
