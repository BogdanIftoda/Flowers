from rest_framework import permissions, viewsets
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

from .models import Item, Order, OrderDetails, Photo, User
from .serializers import (ItemSerializer, OrderDetailsSerializer,
                          OrderSerializer, PhotoSerializer, RegisterSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `get`,`post`, `put`, `patch`, `delete` methods.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RegisterView(CreateAPIView):
    """
        Registration view
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class CurrentUser(APIView):
    """
        Get current user
    """
    authentication_classes = [TokenAuthentication,]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ItemViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `get`,`post`, `put`, `patch`, `delete` methods.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class PhotosList(ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class OrderList(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailsList(ListAPIView):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer
