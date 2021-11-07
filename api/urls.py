from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CurrentUser, OrderDetailsList, OrderList, PhotosList,
                    RegisterView, UserViewSet, ItemViewSet, PhotoViewSet)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'users', UserViewSet)
router.register('photos', PhotoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('current_user/', CurrentUser.as_view()),
    path('photo_list/', PhotosList.as_view()),
    path('order_list/', OrderList.as_view()),
    path('order_details_list/', OrderDetailsList.as_view()),

]


# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication

# # Product Generic Viewset
# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]


# # Category Generic View
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = ProductCategory.objects.all()
#     serializer_class = CategorySerializer
