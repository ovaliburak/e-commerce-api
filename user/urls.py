from django.urls import path 
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='user_register'),
    path('register/employee/', views.EmployeeRegisterAPIView.as_view(), name='employee_register'),
    path('login/', views.LoginAPIView.as_view(), name='user_register'),
    path('logout/', views.LogoutAPIView.as_view(), name='user_logout'),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('list/', views.UserListAPIView.as_view(), name='user_list'),
    path('address/list/', views.UserAddressListAPIView.as_view(), name='user_address_list'),
    path('address/create/', views.UserAddressCreateAPIView.as_view(), name='address_create'),
    path('address/rud/<int:pk>/', views.UserAddressRetrieveUpdateDestroyAPIView.as_view(), name='address_create'),
    # path('address/crete/')


]
