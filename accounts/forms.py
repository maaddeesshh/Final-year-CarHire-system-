from django.contrib.auth.forms import UserCreationForm
from .models import* #from models file import all models



class MyUserCreationForm(UserCreationForm): #define a class that inherits from default django user creation form 
    class Meta:
        model= User 
        fields = [ 'name', 'username', 'email', 'password1','password2'] #define fields to be displayed in the form 
