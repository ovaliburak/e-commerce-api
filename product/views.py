from lib2to3.pgen2 import token
from django.shortcuts import get_object_or_404
from requests import get
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
                            GenericAPIView,
                            ListAPIView,
                            RetrieveAPIView,
                            DestroyAPIView,
                            UpdateAPIView,
                            CreateAPIView,
                        )
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers
from . import models


class CategoryList(ListAPIView):
    serializer_class = serializers.CategoryListSerializer
    queryset = models.Category.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryCreate(CreateAPIView):
    serializer_class = serializers.CategoryCreateSerializer
    queryset = models.Category.objects.all()

    def create(self, request):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CategoryRetrieve(RetrieveAPIView):
    serializer_class = serializers.CategoryRetrieveSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        object = get_object_or_404(models.Category, slug=kwargs['slug'])
        serializer = self.serializer_class(object)
        return Response(serializer.data, status=status.HTTP_200_OK) 

class CategoryUpdate(UpdateAPIView):
    serializer_class = serializers.CategoryUpdateSerializer
    lookup_field = 'slug'

    def put(self, request, *args, **kwargs):
        object = get_object_or_404(models.Category, slug=kwargs['slug'])
        serializer = self.serializer_class(object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        object = get_object_or_404(models.Category, slug=kwargs['slug'])
        serializer = self.serializer_class(object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryDestroy(DestroyAPIView):
    serializer_class = serializers.CategoryDestroySerializer
    lookup_field = 'slug'

    def delete(self, request, *args, **kwargs):
        object = get_object_or_404(models.Category, slug=kwargs['slug'])
        self.perform_destroy(object)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListByCategory(ListAPIView):
    pass


class ProductList(ListAPIView):
    serializer_class = serializers.ProductListSerializer
    permission_classes = (IsAuthenticated, )
    queryset = models.Product.listable.all()

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductCreate(CreateAPIView):
    serializer_class = serializers.ProductCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

'''
List all products available with filters
List all Cattegories 
List all product by categories available with filters

Create Retrieve Update Destroy Product 
Create Destroy Category 
'''