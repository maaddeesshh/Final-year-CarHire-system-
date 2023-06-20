from django.forms import ModelForm
from .models import *

class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        exclude = ['owner']
