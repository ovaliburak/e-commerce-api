from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from user.models import User 
from product.models import Product
from core.models import TimeStampedModel

class Cart(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_cart')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_cart(sender, created, instance, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)
s
class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')
    quantity = models.IntegerField(default=1)
