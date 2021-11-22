from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CurrentUser, ItemViewSet, OrderDetailsViewSet,
                    OrderViewSet, PhotosList, RegisterView, UserViewSet)

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'items', ItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'orderDetails', OrderDetailsViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('items', ItemViewSet.as_view(),),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('current_user/', CurrentUser.as_view()),
    path('photo_list/', PhotosList.as_view()),
]
