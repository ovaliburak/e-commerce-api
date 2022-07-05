from decimal import Decimal
from django.shortcuts import get_object_or_404
from requests import get
from rest_framework.views import APIView
from rest_framework.generics import (
                                    ListAPIView,
                                    CreateAPIView,
                                    RetrieveAPIView,
                                    DestroyAPIView,
                                    UpdateAPIView,
                                    GenericAPIView,
                                    )
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied

from product.models import ProductDiscount, Product
from . import models
from . import serializers


class CartAPIView(APIView):
    def get(self, request):
        user = self.request.user
        cart = get_object_or_404(models.Cart, user=user)
        serializer = serializers.UserCartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CartItemListAPIView(ListAPIView):
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        queryset = models.CartItem.objects.filter(cart__user=self.request.user)
        return queryset

class CreateCartItemAPIView(CreateAPIView):
    serializer_class = serializers.CartSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user 
        cart = get_object_or_404(models.Cart, user=user)
        product = get_object_or_404(models.Product, id=request.data.get('product'))
        current_product = models.CartItem.objects.filter(cart=cart, product=product)
        if current_product.count() > 0:
            raise  NotAcceptable ('You have added already this product on your Cart')
        try:
            quantity = int(request.data.get("quantity", 1))
        except Exception as e:
            raise ValidationError("Please Enter Your Quantity")
        if quantity > product.stock:
            raise NotAcceptable("You order quantity more than the seller have")
        elif quantity < 1:
            raise NotAcceptable("Please enter valid quantity. It must be more than zero or at least equal to one")
        cart_item = models.CartItem(cart=cart, product=product, quantity=quantity)
        cart_item.save()
        serializer = serializers.CartSerializer(cart_item)
        total = float(product.price) * float(quantity)
        cart.total += Decimal(total) 
        cart.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RetrieveCartItemAPIView(RetrieveAPIView):
    serializer_class = serializers.CartSerializer
    queryset = models.CartItem.objects.all()
    def retrieve(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied ("This cart not belong to you!")
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateCartItemAPIView(UpdateAPIView):
    serializer_class = serializers.CartItemUpdateSerializer
    queryset = models.CartItem.objects.all()
    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart = get_object_or_404(models.Cart, user=self.request.user)
        old_quantity = cart_item.quantity
        try: 
            product = get_object_or_404(models.Product, id=request.data.get('product'))
        except Exception as e: 
            raise ValidationError("Product not found!")
        if cart_item.cart.user != request.user: 
            raise PermissionDenied('This item not belong to you')
        try: 
            quantity = request.data.get('quantity', 1)
        except Exception as e: 
            raise NotAcceptable('Please enter quantity')
        if int(quantity) > product.stock: 
            raise ValidationError('You order quantity more than the stock')
        elif int(quantity) < 0:
            raise ValidationError('Your quantity must be more zero or at least equal to one')
        serializer = self.get_serializer(cart_item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if int(old_quantity) > int(quantity):
            cart.total -= Decimal(float(product.price) * float(int(old_quantity)-
                                                                int(quantity)))
        elif int(old_quantity) == int(quantity):
            pass 
        else:
            cart.total += Decimal(float(product.price) * float(quantity))
        cart.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class DeleteCartItemAPIView(DestroyAPIView):
    queryset = models.CartItem.objects.all()
    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied("This item not belong to you.")
        cart = get_object_or_404(models.Cart, user=self.request.user)
        product_price = cart_item.product.price 
        quantity = cart_item.quantity 
        total = float(product_price) * float(quantity)
        cart_item.delete()
        cart.total -= Decimal(total)
        if cart.total < 0 or not models.CartItem.objects.all().exists():
            cart.total = 0.00
        cart.save()
        return Response({'message':'item successfull destroyed'}, 
                        status=status.HTTP_204_NO_CONTENT)



# class AddToCartAPIView(APIView):
#     def post(self, request, *args, **kwargs):

#         id = request.data.get('id')
#         if id is None:
#             return Response({'Message':'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
        
#         item = get_object_or_404(Product, id=id)
#         print(item)

#         return Response(status=status.HTTP_200_OK)

# class CreateCartAPIVies(ListCreateAPIView):
#     queryset = models.Cart.objects.all()
#     serializer_class = serializers.CartCreateSerializer

#     def get(self, request):
#         print(self.get_queryset())
#         serializer = self.get_serializer(self.get_queryset(), many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def create(self, request, *args, **kwargs):
#         user = request.user 
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=user)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



    