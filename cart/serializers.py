from rest_framework import serializers

from . import models 
from product.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta: 
        model = models.CartItem
        fields = '__all__'

class UserCartSerializer(serializers.ModelSerializer):
    cart_item = CartSerializer(many=True)
    class Meta: 
        model = models.Cart
        fields = ['total', 'cart_item']

class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ["product", "quantity"]