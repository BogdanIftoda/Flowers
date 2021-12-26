from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, serializers, viewsets
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Item, Order, OrderDetails, Photo, User
from .serializers import (ItemPhotoSerializer, ItemSerializer,
                          OrderDetailsItemsSerializer, OrderDetailsSerializer,
                          OrderSerializer, OrderUserSerializer,
                          PhotoSerializer, RegisterSerializer, UserSerializer)
from django.shortcuts import get_object_or_404
from rest_framework import status


current_user = openapi.Response('', UserSerializer)

@method_decorator(name='update', decorator=swagger_auto_schema(request_body=UserSerializer))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(request_body=UserSerializer))
class UserViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
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
    permission_classes = (permissions.IsAuthenticated, )

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


@method_decorator(name='update', decorator=swagger_auto_schema(request_body=OrderSerializer))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(request_body=OrderSerializer))
class OrderViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrderSerializer
        return OrderUserSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@method_decorator(name='update', decorator=swagger_auto_schema(request_body=OrderDetailsSerializer))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(request_body=OrderDetailsSerializer))
class OrderDetailsViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin):
    serializer_class = OrderDetailsSerializer
    # permission_classes = (permissions.IsAuthenticated, )
    def get_queryset(self):
        user = self.request.user
        order_detail = OrderDetails.objects.filter(user=user)
        return order_detail

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrderDetailsSerializer
        return OrderDetailsItemsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddToCartAPIView(GenericAPIView):

    def get(self, request, pk):
        user = request.user
        print(user)
        item = get_object_or_404(Item, id=pk)
        ordered_product_qs = OrderDetails.objects.filter(
            item=item)
        if ordered_product_qs.exists():
            ordered_product = ordered_product_qs[0]
            ordered_product.quantity += 1
            ordered_product.save()
            return Response({'success': 'item quantity updated'}, status=status.HTTP_200_OK)
        else:
            order_qs = Order.objects.filter(user=user)
            ordered_product = OrderDetails.objects.create(
                user=user, item=item)

            if order_qs.exists():
                order = order_qs[0]
                order.order_detail_items.add(ordered_product)
                order.save()
                return Response({'success': 'item added to your cart'}, status=status.HTTP_200_OK)

            else:
                order = Order.objects.create(user=user)
                order.order_detail_items.add(ordered_product)
                order.save()
                return Response({'success': 'item added to your cart'}, status=status.HTTP_200_OK)

