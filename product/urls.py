from django.urls import path
from . import views

urlpatterns = [
    path('category/list/', views.CategoryList.as_view(), name='category_list'),
    path('category/create/', views.CategoryCreate.as_view(), name='category_create'),
    path('category/retrieve/<slug:slug>/', views.CategoryRetrieve.as_view(), 
        name='category_retrieve'),
    path('category/update/<slug:slug>/', views.CategoryUpdate.as_view(), 
        name='category_update'),
    path('category/delete/<slug:slug>/', views.CategoryDestroy.as_view(), 
        name='category_delete'),
    path('list/', views.ProductList.as_view(), name='product_list'),
    path('create/', views.ProductCreate.as_view(), name='product_create'),
]
