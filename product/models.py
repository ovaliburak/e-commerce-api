import uuid
from django.db import models
from django.utils.text import slugify
from core.models import TimeStampedModel
from core.managers import ProductManager
from . import choices

    
class ProductVariant(models.Model): #BUG
    color = models.CharField(db_index=True, max_length=15, choices=choices.COLOR_CHOICES, blank=True, null=True)
    size = models.CharField(db_index=True, max_length=3, choices=choices.SIZE_CHOICES, blank=True, null=True)
    capacity = models.CharField(db_index=True, max_length=15, choices=choices.CAPACITY_CHOICES, blank=True, null=True )
    
    def __str__(self):
        if self.color and self.size:
            return(self.color, self.size)
        elif self.color and self.capacity:
            return (self.color, self.capacity)
        else:
            return ('BUG')
        
class Category(TimeStampedModel):
    name = models.CharField(db_index=True, max_length=100, null=False, blank=False, unique=True)
    desc = models.TextField(null=True, blank=True)
    slug = models.SlugField(blank=False, null=False, unique=True)
    # variant = models.ManyToManyField(ProductVariant, related_name='category')


    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# class ProductInventory(TimeStampedModel):
#     quantity = models.IntegerField(blank=False, null=False, default=0)

#     def __str__(self):
#         return str(self.quantity)

class ProductDiscount(TimeStampedModel):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    discount_percent = models.FloatField()
    discount_quantity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=0.00)
    active = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name
    

class Product(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True, null=False, default='There is no desc.')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    stock = models.IntegerField(default=0)
    price = models.DecimalField(db_index=True, max_digits=6, decimal_places=2, blank=False, null=False, default=0.00)
    product_discount = models.ForeignKey(ProductDiscount, on_delete=models.DO_NOTHING, related_name='product', 
                                            null=True, blank=True)
    is_listable = models.BooleanField(default=False)

    objects = models.Manager() 
    listable = ProductManager() 

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
    