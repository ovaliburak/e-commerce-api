from django.urls import path
from . import views

urlpatterns = [
    ##Category
    path('category/list/', views.CategoryList.as_view(), name='category_list'),
    path('category/list_product/', views.CategoryProductList.as_view(), name='category_list_product'),
    path('category/create/', views.CategoryCreate.as_view(), name='category_create'),
    path('category/retrieve/<slug:slug>/', views.CategoryRetrieve.as_view(), 
        name='category_retrieve'),
    path('category/update/<slug:slug>/', views.CategoryUpdate.as_view(), 
        name='category_update'),
    path('category/delete/<slug:slug>/', views.CategoryDestroy.as_view(), 
        name='category_delete'),
    ##Product    
    path('list/', views.ProductList.as_view(), name='product_list'),
    path('create/', views.ProductCreate.as_view(), name='product_create'),
    path('retrieve/<uuid:pk>', views.ProductRetrieve.as_view(), name='product_retrieve'),
    path('update/<uuid:pk>', views.ProductUpdate.as_view(), name='product_update'),
    path('delete/<uuid:pk>', views.ProductDestroy.as_view(), name='product_delete'),
]
