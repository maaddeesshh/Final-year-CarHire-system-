from django.db import models
import datetime
from accounts.models import User

from django.core.validators import RegexValidator

# Create your models here.

# Create the Car Model
class Car(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=20, unique=True, validators=[
        RegexValidator('^(K)([ABCDEFGHJKLMNPQRSTUVWXYZ]){2}( ){1}(\d){3}([ABCDEFGHJKLMNPQRSTUVWXYZ])$',
                       message="Invalid Number Plate")])
    image = models.ImageField(upload_to='car_images/')
    description = models.TextField(null=True, blank=True)
    phone_no = models.CharField(max_length=20, unique=True,
                                validators=[RegexValidator('^(0)([127])(\d){8}$', message='Invalid phone numbers')])
    updated = models.DateTimeField(auto_now = True , null=True)
    created = models.DateTimeField(auto_now_add=True, null= True)

    class Meta:
       ordering = ['-updated', '-created']  # Order by updated field in descending order and then by created field in descending order

  

    def __str__(self):
        return self.reg_no
