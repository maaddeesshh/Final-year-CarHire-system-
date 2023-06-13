from django.conf import settings
from django.db import models

    
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True,null=True)



USERNAME_FIELD = 'username'
REQUIRED_FIELDS = []