from django.contrib.auth.models import BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, birth_year,password=None):
        if (not email
            or not first_name 
            or not last_name 
            or not password 
            or not birth_year):
            raise ValueError('The user must have all the fields.')
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            birth_year = birth_year,
        )

        user.set_password(password)
        user.save()
        return user 

    
    def create_superuser(self, email, first_name, last_name, birth_year,password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            birth_year=birth_year,
            password=password
        )       
        user.is_admin = True 
        user.save()
        return user


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_listable=True)
