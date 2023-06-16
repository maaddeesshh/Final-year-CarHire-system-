from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import * #from models file import all models
from django.contrib.auth.models import Group
from .forms import * #from forms file import all forms


#authenticate, login user
def LoginPage(request):
     page = 'login'
     msg= None
     if request.user.is_authenticated:
          return redirect('home') #if a user is already authenticated, take the user to homepage
     if request.method == "POST":
          username = request.POST.get('username') # get username from user form input, asign to variable username
          password = request.POST.get('password') # get password from user form input, asign to variable password

          try:
               user = User.objects.get(username=username)
          except:
               msg= 'User does not exist' 
          user= authenticate(request, username=username, password=password)

          if user is not None and user.groups.filter(name='customer').exists():
             login(request, user)
             return redirect('customer_dashboard')#after successful authentication, redirect user to dashboard according to role
          elif user is not None and user.groups.filter(name='owner').exists():
             login(request, user)
             return redirect('owner_dashboard')

          
          else:
               msg='username or password is incorrect'      
     context={'msg':msg, 'page':page}
     return render(request, 'accounts/login_register.html', context)
#logout user, redirect to home
def logoutUser(request):
     logout(request)
     return redirect('home')
#register a new user
def registerPage(request):
     msg = None
     if request.user.is_authenticated: #if a user is already authenticated, take the user to homepage
          return redirect('home')
     form= MyUserCreationForm() #assign variable form to MyUserCreationForm, in forms.py
     if request.method == 'POST':   # check form method from front-end
          form = MyUserCreationForm(request.POST)
          if form.is_valid(): #check if form is valid
               user = form.save(commit=False) #capture, save and commit to access the created user so that we clean the inputs  
               user.username=user.username.lower()
               user.save() #save user
               return redirect('login')
          else:
               msg= 'An error occurred during registration' 
     return render(request, 'accounts/login_register.html', {'form':form, 'msg':msg})
@login_required #to ensure the request user is authenticated and is logged in
#owner  update profile 
def OwnerUpdateProfile(request):
    msg = None
    user = request.user
    form = MyUserCreationForm(instance=user)#request user details displayed in the form 
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            msg = 'Your account has been updated successfully.'
            return redirect('home')
        else:
            msg = 'An error occurred during account update.'

    return render(request, 'accounts/Owner_Update.html', {'form': form, 'msg': msg})

@login_required
#owner  delete profile 
def OwnerdeleteAccount(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('home') #redirect to home page 
    
    return render(request, 'accounts/Owner_delete_account.html')

@login_required
#customer  update profile 
def UpdateProfile(request):
    msg = None
    user = request.user
    form = MyUserCreationForm(instance=user)
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            msg = 'Your account has been updated successfully.'
            return redirect('home')
        else:
            msg = 'An error occurred during account update.'

    return render(request, 'accounts/Customer_Update.html', {'form': form, 'msg': msg})


@login_required
#customer  delete profile 
def deleteAccount(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('home')
    
    return render(request, 'accounts/Customer_delete_account.html')



def customerPage(request):
      return render(request, 'accounts/customer_dashboard.html')

def ownerPage(request):
     return render(request, 'accounts/owner_dashboard.html')
def home(request):
    return render(request,'accounts/home.html')

def AboutUs(request):
    return render(request,'accounts/about.html')  

def Contact(request):
    return render(request,'accounts/contact.html')  


def Service(request):
    return render(request,'accounts/services.html') 


def Terms(request):
    return render(request,'accounts/Terms.html')


