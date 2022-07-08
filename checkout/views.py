from itertools import product
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import User, UserAddress
from cart.models import Cart, CartItem

from cart.serializers import CartSerializer, UserCartSerializer
from product.serializers import ProductSerializer, ProductDiscountSerializer
from user.serializers import UserAddressSerializer, UserSerializer
from .serializers import CheckOutCartItemSerializer, CheckOutAddressSerializer


class CheckOutAPIView(APIView): 
    def get(self, request, *args, **kwargs):
        user = self.request.user 
        cart = Cart.objects.get(user=user)
        address = get_object_or_404(UserAddress, user=user)
        data = {}
        items = CheckOutCartItemSerializer(CartItem.objects.filter(cart=cart), many=True).data
        # for item in items:
        #     print(item['product'].get('name'))
        data['items'] = items
        data['address'] = CheckOutAddressSerializer(address).data
        data['total'] = UserCartSerializer(cart).data.get('total')
        return Response(data, status=status.HTTP_200_OK)
