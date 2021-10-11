from django.urls import path
from .views import BoquetInfoList, ItemList, OrderDetailsList, OrderList, PhotosList, UsersList, RegisterView


urlpatterns = [
    path('user_list/', UsersList.as_view()),
    path('item_list/', ItemList.as_view()),
    path('photo_list/', PhotosList.as_view()),
    path('order_list/', OrderList.as_view()),
    path('boquet_info_list/', BoquetInfoList.as_view()),
    path('order_details_list/', OrderDetailsList.as_view()),
    path('register/', RegisterView.as_view(), name='auth_register'),
]
