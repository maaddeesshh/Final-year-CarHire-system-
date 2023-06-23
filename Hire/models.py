
import datetime

from django.core.validators import MinValueValidator, RegexValidator
from Owner.models import Car
from django.db import models

# This is used to import the user Model
from accounts.models import User

# Create Hire models here.
class Hire(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    from_destination = models.CharField(max_length=20, null="True", validators=[
        RegexValidator("^([a-zA-Z])[a-zA-Z'\d ]+$", message='Must be a valid name of a place')])
    to_destination = models.CharField(max_length=20, null=True, validators=[
        RegexValidator("^([a-zA-Z])[a-zA-Z'\d ]+$", message='Must be a valid name of a place')])
    start_date = models.DateField(
        validators=[MinValueValidator(datetime.date.today(), "Start date can not be less than today")])
    end_date = models.DateField(
        validators=[MinValueValidator(datetime.date.today(), "Start date can not be less than today")])
    phone_no = models.CharField(max_length=20, null="True",
                                validators=[RegexValidator('^(0)([127])(\d){8}$', message='Invalid phone numbers')])
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)