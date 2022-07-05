from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartAPIView.as_view(), name='user_cart'),
    path('list/', views.CartItemListAPIView.as_view(), name='cart_item_list'),
    path('create/', views.CreateCartItemAPIView.as_view(), name='create_cart_item'),
    path('retrieve/<int:pk>/', views.RetrieveCartItemAPIView.as_view(), name='retrieve_cart_item'),
    path('update/<int:pk>/', views.UpdateCartItemAPIView.as_view(), name='update_cart_item'),
    path('delete/<int:pk>/', views.DeleteCartItemAPIView.as_view(), name='delete_cart_item'),

    
]
