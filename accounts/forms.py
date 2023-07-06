from django.contrib.auth.forms import UserCreationForm
from .models import* #from models file import all models
from Hire.models import Hire
from django import forms
# from Ratings.models import Review, RATE_CHOICES



class MyUserCreationForm(UserCreationForm): #define a class that inherits from default django user creation form 
    class Meta:
        model= User 
        fields = [ 'name', 'username', 'email', 'password1','password2'] #define fields to be displayed in the form 



class HireForm(forms.ModelForm):
    class Meta:
        model = Hire
        fields = ['start_date', 'end_date', 'from_destination','to_destination','phone_no']




class RateForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=False)
	rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)

	class Meta:
		model = Review
		fields = ('text', 'rate')
