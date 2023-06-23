from django.contrib.auth.forms import UserCreationForm
from .models import* #from models file import all models
from Hire.models import Hire
from django import forms



class MyUserCreationForm(UserCreationForm): #define a class that inherits from default django user creation form 
    class Meta:
        model= User 
        fields = [ 'name', 'username', 'email', 'password1','password2'] #define fields to be displayed in the form 



class HireForm(forms.ModelForm):
    class Meta:
        model = Hire
        fields = ['start_date', 'end_date', 'from_destination','to_destination','phone_no']