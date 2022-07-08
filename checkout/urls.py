from django.urls import path
from . import views

urlpatterns = [
    path('', views.CheckOutAPIView.as_view(), name='checkout'),
    
]
