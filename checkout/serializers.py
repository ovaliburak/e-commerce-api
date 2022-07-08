from dataclasses import field, fields
from rest_framework import serializers

from product.models import Product
from cart.models import CartItem
from user.models import UserAddress


class CheckOutProductSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = ['name', 'price']

class CheckOutCartItemSerializer(serializers.ModelSerializer):
    product = CheckOutProductSerializer()
    total = serializers.SerializerMethodField()
    class Meta: 
        model = CartItem
        fields = ['product','quantity', 'total']
    
    def get_total(self, obj):
        return float(obj.product.price) * float(obj.quantity)

class CheckOutAddressSerializer(serializers.ModelSerializer):
    class Meta: 
        model = UserAddress
        fields = [
            'address_line1',
            'address_line2',
            'city',
            'postal_code',
            'country',
            'phone',
        ]
    
