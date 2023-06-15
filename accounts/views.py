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
from .models import *
from django.contrib.auth.models import Group
from .forms import *

def LoginPage(request):
     page = 'login'
     msg= None
     if request.user.is_authenticated:
          return redirect('home')
     if request.method == "POST":
          username = request.POST.get('username')
          password = request.POST.get('password')

          try:
               user = User.objects.get(username=username)
          except:
               msg= 'User does not exist' 
          user= authenticate(request, username=username, password=password)

          if user is not None and user.groups.filter(name='customer').exists():
             login(request, user)
             return redirect('customer_dashboard')
          elif user is not None and user.groups.filter(name='owner').exists():
             login(request, user)
             return redirect('owner_dashboard')

          
          else:
               msg='username or password is incorrect'      
     context={'msg':msg, 'page':page}
     return render(request, 'accounts/login_register.html', context)
def logoutUser(request):
     logout(request)
     return redirect('home')
def registerPage(request):
     msg = None
     if request.user.is_authenticated:
          return redirect('home')
     form= MyUserCreationForm()
     if request.method == 'POST':
          form = MyUserCreationForm(request.POST)
          if form.is_valid():
               user = form.save(commit=False)
               user.username=user.username.lower()
               user.save()
               return redirect('login')
          else:
               msg= 'An error occurred during registration' 
     return render(request, 'accounts/login_register.html', {'form':form, 'msg':msg})
@login_required
def OwnerUpdateProfile(request):
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

    return render(request, 'accounts/Owner_Update.html', {'form': form, 'msg': msg})

@login_required
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



def customerPage(request):
      return render(request, 'accounts/customer_dashboard.html')

def ownerPage(request):
     return render(request, 'accounts/owner_dashboard.html')
def home(request):
    return render(request,'accounts/home.html')

def AboutUs(request):
    return render(request,'accounts/about.html')  
