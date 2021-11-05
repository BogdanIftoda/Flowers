from django.urls import path
from .views import BoquetInfoList, ItemList, OrderDetailsList, OrderList, PhotosList, UsersList, RegisterView, ItemDetail


urlpatterns = [
    path('user_list/', UsersList.as_view()),
    path('item_list/', ItemList.as_view()),
    path('item_detail/<int:item_id>/', ItemDetail.as_view()),
    path('photo_list/', PhotosList.as_view()),
    path('order_list/', OrderList.as_view()),
    path('boquet_info_list/', BoquetInfoList.as_view()),
    path('order_details_list/', OrderDetailsList.as_view()),
    path('register/', RegisterView.as_view(), name='auth_register'),
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
