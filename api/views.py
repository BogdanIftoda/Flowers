from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, serializers
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from .models import Item, Order, OrderDetails, Photo, User
from .serializers import (ItemPhotoSerializer, ItemSerializer,
                          OrderDetailsItemsSerializer, OrderDetailsSerializer,
                          OrderSerializer, OrderUserSerializer,
                          PhotoSerializer, RegisterSerializer, UserSerializer, GetOrderSerializer)
from django.shortcuts import get_object_or_404
from rest_framework import status


current_user = openapi.Response('', UserSerializer)
get_orders = openapi.Response('', OrderSerializer)

@method_decorator(name='update', decorator=swagger_auto_schema(request_body=UserSerializer))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(request_body=UserSerializer))
class UserViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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




class OrderViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin,
                  DestroyModelMixin):
    queryset = Order.objects.all()
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderSerializer
        return OrderUserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        order_serializer = OrderSerializer(data=data)
        order_serializer.is_valid(raise_exception=True)
        user = request.user
        items = data['order_detail_items']
        for pk in items:
            item = get_object_or_404(Item, id=pk)
            order_qs = Order.objects.filter(user=user, created=False)
            ordered_product = OrderDetails.objects.create(
                user=user, item=item)
            item.in_stock -= ordered_product.quantity
            item.save()
            if order_qs.exists():
                order = order_qs[0]
                order.order_detail_items.add(ordered_product)
                order.save()
            else:
                order = Order.objects.create(user=user)
                order.delivery_address = data['delivery_address']
                order.order_detail_items.add(ordered_product)
                order.save()
        order = Order.objects.get(user=user, created=False)
        order.created = True
        order.total = order.get_order_total()
        order.save()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: get_orders})
    @action(detail=False, methods=['get'])
    def get_orders(self, request):
        queryset = Order.objects.filter(user=request.user, created=True)
        print(queryset)
        serializer = GetOrderSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


@method_decorator(name='update', decorator=swagger_auto_schema(request_body=OrderDetailsSerializer))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(request_body=OrderDetailsSerializer))
class OrderDetailsViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin):
    serializer_class = OrderDetailsSerializer
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