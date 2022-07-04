'''
List all products available with filters
List all Cattegories 
List all product by categories available with filters

Create Retrieve Update Destroy Product 
Create Destroy Category 
'''

from rest_framework import serializers 
from rest_framework.reverse import reverse

from . import models 

#PRODUCT SERIALIZER

class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.ProductDiscount
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    # discount = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='product_retrieve')
    edit_url = serializers.HyperlinkedIdentityField(view_name='product_update')
    delete_url = serializers.HyperlinkedIdentityField(view_name='product_delete')
    product_discount = ProductDiscountSerializer(read_only=True)

    class Meta: 
        model = models.Product
        fields = '__all__'


    def get_discount(self, obj):
         return obj.get_discount()

    # def get_url(self, obj):
    #     # return f"/api/product/category/retrieve/{obj.slug}/"
    #     request = self.context.get('request') #self.request
    #     if request is None:
    #         return None 
    #     return reverse("product_retrieve", kwargs={"slug": obj.slug}, request=request)

class ProductSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.Product
        fields = '__all__'

##CATEGORY SERIALIZERS

class CategoryListSerializer(serializers.ModelSerializer):
    edit_url = serializers.HyperlinkedIdentityField(view_name='category_update',
                                                    lookup_field='slug')
    url = serializers.SerializerMethodField(read_only=True)
    current_user = serializers.SerializerMethodField(read_only=True)
    product = ProductListSerializer(many=True)
    
    class Meta:
        model = models.Category
        fields = '__all__'
    
    def get_url(self, obj):
        # return f"/api/product/category/retrieve/{obj.slug}/"
        request = self.context.get('request') #self.request
        if request is None:
            return None 
        return reverse("category_retrieve", kwargs={"slug": obj.slug}, request=request)
    
    def get_current_user(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
           return request.user.email
        return None

class CategoryProductListSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(many=True, read_only=True)
    class Meta: 
        model = models.Category
        fields = ['name', 'product']

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model = models.Category 
        fields = '__all__'
    

        
 