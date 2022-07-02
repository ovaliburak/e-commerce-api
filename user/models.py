import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken
import datetime

from core.models import TimeStampedModel
from core.managers import UserManager


class User(AbstractBaseUser):
    YEAR_CHOICES = []
    for r in range((datetime.datetime.now().year-100), 
                    (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(db_index=True, blank=False, null=False, unique=True)
    first_name = models.CharField(db_index=True, blank=False, null=False, max_length=100)
    last_name = models.CharField(db_index=True, blank=False, null=False, max_length=100)
    birth_year = models.IntegerField(choices=YEAR_CHOICES ,blank=False, null=False)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birth_year']


    def __str__(self):
        return self.email

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
class Profile(TimeStampedModel):
    pass 