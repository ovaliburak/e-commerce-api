from django.urls import path 
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user_register'),
    path('login/', views.LoginAPIView.as_view(), name='user_register'),
    path('logout/', views.LogoutAPIView.as_view(), name='user_logout'),
    path('example/', views.ExampleAPIView.as_view(), name='example'),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),

]
