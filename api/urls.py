from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CurrentUser, ItemViewSet, OrderDetailsViewSet,
                    OrderViewSet, PhotosList, RegisterView, UserViewSet, AddToCartAPIView)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='items')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'orderDetails', OrderDetailsViewSet, basename='orderDetails')
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('add-to-cart/<int:pk>/', AddToCartAPIView.as_view(), name='addToCart'),
    path('current_user/', CurrentUser.as_view()),
    path('photo_list/', PhotosList.as_view()),
]
