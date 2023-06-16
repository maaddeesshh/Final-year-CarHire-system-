from django.conf import settings
from django.db import models

    
from django.contrib.auth.models import AbstractUser # import an abstract user model which is a child of the  django user model
#define a model user that inherits from AbstractUser model
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True) #attribute name defined
    email = models.EmailField(unique=True,null=True)



USERNAME_FIELD = 'username' #username field defined 
REQUIRED_FIELDS = []