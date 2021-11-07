from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Item, Order, OrderDetails, Photo, User
from .serializers import (ItemSerializer,
                          OrderDetailsSerializer, OrderSerializer,
                          PhotoSerializer, UserSerializer, RegisterSerializer)
from rest_framework.response import Response

from .permissions import IsAuthorOrReadOnly


from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `get`,`post`, `put`, `patch`, `delete` methods.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


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

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ItemViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `get`,`post`, `put`, `patch`, `delete` methods.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class UsersList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated, )


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
