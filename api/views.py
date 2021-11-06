from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Item, Order, OrderDetails, Photo, User
from .serializers import (ItemSerializer,
                          OrderDetailsSerializer, OrderSerializer,
                          PhotoSerializer, UserSerializer, RegisterSerializer)
from django.http import Http404
from rest_framework.response import Response

class RegisterView(CreateAPIView):
    """
        Registration view
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class ItemDetail(APIView):
    """
        Item detail view
    """
    def get_object(self, item_id):
        try:
            return Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise Http404
    
    def get(self, request, item_id):
        item = self.get_object(item_id)
        serializer = ItemSerializer(item)
        return Response(serializer.data)


class UsersList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated, permissions.)


class ItemList(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # permission_classes = (
    #     permissions.IsAuthenticated,)


class PhotosList(ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    # permission_classes = (
        # permissions.IsAuthenticated,)


class OrderList(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (
        permissions.IsAuthenticated,)

class OrderDetailsList(ListAPIView):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer
    permission_classes = (
        permissions.IsAuthenticated,)

