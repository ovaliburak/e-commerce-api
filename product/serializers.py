'''
List all products available with filters
List all Cattegories 
List all product by categories available with filters

Create Retrieve Update Destroy Product 
Create Destroy Category 
'''

from rest_framework import serializers 

from . import models 

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name', 'desc']

class CategoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name','desc', 'slug']

class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name', 'desc', 'slug']

class CategoryDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    
    class Meta: 
        model = models.Product
        fields = ['name','category']

class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta: 
        model = models.Product
        fields = [
                'name',
                'desc',
                'category',
                'product_inventory',
                'price',
                'product_discount',
                'is_listable']

    

        
 