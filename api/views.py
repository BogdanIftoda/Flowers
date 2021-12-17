from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Item, Order, OrderDetails, Photo, User
from .serializers import (ItemSerializer, OrderDetailsSerializer,
                          OrderSerializer, PhotoSerializer, RegisterSerializer,
                          UserSerializer, ItemPhotoSerializer)

current_user = openapi.Response('', UserSerializer)


@method_decorator(name='update', decorator=swagger_auto_schema(request_body=UserSerializer))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(request_body=UserSerializer))
class UserViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,)


@method_decorator(name='create', decorator=swagger_auto_schema(request_body=RegisterSerializer))
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

    authentication_classes = [JWTAuthentication, ]

    @swagger_auto_schema(tags=['current user'], responses={200: current_user})
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


@method_decorator(name='update', decorator=swagger_auto_schema(request_body=ItemSerializer))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(request_body=ItemSerializer))
class ItemViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin):
    queryset = Item.objects.all()
    # permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ItemSerializer
        return ItemPhotoSerializer

class PhotosList(ListAPIView):
    """
         Get current user
     """

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    @swagger_auto_schema(tags=['photo list'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer
