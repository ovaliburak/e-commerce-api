from django.urls import path 
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='user_register'),
    path('register/employee/', views.EmployeeRegisterAPIView.as_view(), name='employee_register'),
    path('login/', views.LoginAPIView.as_view(), name='user_register'),
    path('logout/', views.LogoutAPIView.as_view(), name='user_logout'),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),

]
