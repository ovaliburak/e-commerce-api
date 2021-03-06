from django.shortcuts import get_object_or_404
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
from core.permissions import EmployeeUserOnly

##CATEGORY VIEWS

class CategoryList(ListAPIView):
    serializer_class = serializers.CategoryListSerializer
    queryset = models.Category.objects.all()
    permission_classes = (AllowAny, )
    lookup_field = 'slug'

    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) #BUG

class CategoryProductList(ListAPIView):
    serializer_class = serializers.CategoryProductListSerializer
    queryset = models.Category.objects.all()
    permission_classes = (AllowAny, )


    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryCreate(CreateAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    permission_classes = (EmployeeUserOnly, )

    def create(self, request):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)   
        
    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        desc = serializer.validated_data.get('desc', None)
        if desc is None:
            desc = name 
        serializer.save(desc=desc)  

class CategoryRetrieve(RetrieveAPIView):
    serializer_class = serializers.CategorySerializer
    permission_classes = (AllowAny, )

    def retrieve(self, request, *args, **kwargs):
        object = get_object_or_404(models.Category, slug=kwargs['slug'])
        serializer = self.serializer_class(object)
        return Response(serializer.data, status=status.HTTP_200_OK) 

class CategoryUpdate(UpdateAPIView):
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'
    queryset = models.Category.objects.all()
    permission_classes = (EmployeeUserOnly, )

    def put(self, request, *args, **kwargs):
        object = get_object_or_404(models.Category, slug=kwargs['slug'])
        serializer = self.get_serializer(object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CategoryDestroy(DestroyAPIView):
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'
    permission_classes = (EmployeeUserOnly, )

    def delete(self, request, *args, **kwargs):
        object = get_object_or_404(models.Category, slug=kwargs['slug'])
        self.perform_destroy(object)
        return Response(status=status.HTTP_204_NO_CONTENT)

##PRODUCT VIEWS

class ProductList(ListAPIView):
    serializer_class = serializers.ProductListSerializer
    permission_classes = (AllowAny, )
    queryset = models.Product.listable.all()

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        self.check_object_permissions(request, serializer)
        print(self.check_object_permissions(request, serializer))
        self.check_permissions(request)
        print(self.check_permissions(request))
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductCreate(CreateAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = (EmployeeUserOnly, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def perform_create(self, serializer):
        serializer.save()

class ProductRetrieve(RetrieveAPIView):
    queryset = models.Product.listable.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (AllowAny, )
    
    def retrieve(self, request, *args, **kwargs):
        object = get_object_or_404(models.Product, pk=kwargs['pk'])
        serializer = self.get_serializer(object)
        return Response(serializer.data, status=status.HTTP_200_OK) 
   
class ProductUpdate(UpdateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (EmployeeUserOnly, )


class ProductDestroy(DestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer()
    permission_classes = (EmployeeUserOnly, )


'''

List all products available with filters
List all Cattegories 
List all product by categories available with filters

Create Retrieve Update Destroy Product 
Create Destroy Category 
'''