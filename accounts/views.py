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
from Owner.models import Car
from django.http import HttpResponse, HttpResponseRedirect
from Owner.forms import CarForm
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from Hire.models import Hire
from datetime import date
from datetime import timedelta




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
     msg1 = None
     msg2 = None
     msg3 = None
     msg5 = None
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
               msg= 'Your password should be alphanumeric'
               msg2='First letter of the password should be capital'
               msg3=' Password must contain a special character (@, $, !, &, etc).'
               msg1=' Password length must be greater than 8 characters.' 
               msg5 ='Enter same password for verification and provide a unique email'
     return render(request, 'accounts/login_register.html', {'form':form, 'msg':msg, 'msg2':msg2,'msg':msg,'msg3':msg3, 'msg1':msg1, 'msg5':msg5})
@login_required(login_url='login')  #to ensure the request user is authenticated and is logged in
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

@login_required(login_url='login') 
#owner  delete profile 
def OwnerdeleteAccount(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('home') #redirect to home page 
    
    return render(request, 'accounts/Owner_delete_account.html')

@login_required(login_url='login') 
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


@login_required(login_url='login') 
#customer  delete profile 
def deleteAccount(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('home')
    
    return render(request, 'accounts/Customer_delete_account.html')



def customerPage(request):
    
    cars = Car.objects.all()
    context = {'cars':cars} 
    return render(request, 'accounts/customer_dashboard.html',context)

def ownerPage(request):
     cars = Car.objects.all()
     notification_count = Hire.objects.filter(car__in=cars, is_approved=False, is_rejected=False).count()
    
     context = {'cars':cars,'notification_count': notification_count} 


     return render(request, 'accounts/owner_dashboard.html' , context)
@login_required(login_url='login') 
def updateCar(request, pk):
     car = Car.objects.get(id=pk)
     form = CarForm(instance=car)
     if request.user != car.owner:
          return HttpResponse('<h1 style="color: red;">You are not allowed here!!!</h1>')

     if request.method == 'POST':
          form = CarForm(request.POST, instance=car)
          if form.is_valid:
               form.save()
               return redirect('owner_dashboard')
     context={'form':form}
     return render(request, 'Owner/createcar.html', context)

@login_required(login_url='login') 
def deleteCar(request, pk):
     car = Car.objects.get(id=pk)
     if request.user != car.owner:
          return HttpResponse('<h1 style="color: red;">You are not allowed here!!!</h1>')
     if request.method == 'POST':
          car.delete()
          return redirect('owner_dashboard')  
     return render(request, 'accounts/delete.html', {'obj':car})

# @login_required(login_url='login')
# def hire_car(request, pk):
#     car = get_object_or_404(Car, pk=pk)
#     user = user=request.user
#     form = HireForm()

#     if request.method == 'POST':
#         form = HireForm(request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']

#             if end_date < start_date:
#                 return render(request, 'accounts/hire.html', {'form': form, 'book_error': 'End date cannot be earlier than the start date'})

#             # Get all future hires
#             booked_times = Hire.objects.filter(car=car, end_date__gte=date.today(), is_approved=True)
            
#             if booked_times.exists():
#                 return render(request, 'accounts/hire.html', {'form': form, 'booked_times': booked_times})

#             hire = form.save(commit=False)
#             hire.car = car
#             hire.customer = user
#             hire.save()
#             return redirect('success')


#     context = {
#         'form': form,
#         'car': car
#     }

#     return render(request, 'accounts/hire.html' ,context)

@login_required(login_url='login')
def hire_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    user = request.user
    form = HireForm()

    if request.method == 'POST':
        form = HireForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            if end_date < start_date:
                return render(request, 'accounts/hire.html', {'form': form, 'book_error': 'End date cannot be earlier than the start date'})

            # Get all approved hires for the car
            approved_hires = Hire.objects.filter(car=car, is_approved=True)

            for approved_hire in approved_hires:
                # Check if the requested hire overlaps with an approved hire
                if start_date <= approved_hire.end_date and end_date >= approved_hire.start_date:
                    # Check if the approved hire has already ended
                    if approved_hire.end_date < date.today() or (end_date + timedelta(days=1)) < approved_hire.start_date:
                        continue  # Skip the check for this approved hire if it has already ended or the user's end date is a day before the approved hire's start date

                    return render(request, 'accounts/hire.html', {'form': form, 'booked_times': approved_hires})

            hire = form.save(commit=False)
            hire.car = car
            hire.customer = user
            hire.save()
            return redirect('success')

    context = {
        'form': form,
        'car': car
    }

    return render(request, 'accounts/hire.html', context)



def success(request):
    return render(request,'accounts/success.html' )
@login_required(login_url='login')
def customer_hire_requests(request):
    user = request.user
    hires = Hire.objects.filter(customer=user)
    return render(request, 'accounts/customer_hire_requests.html', {'hires': hires})


@login_required(login_url='login')
def update_hire(request, pk):
    hire = get_object_or_404(Hire, pk=pk)
    form = HireForm(instance=hire)

    if request.method == 'POST':
        form = HireForm(request.POST, instance=hire)
        if form.is_valid():
            form.save()
            return redirect('customer_dashboard')

    context = {
        'form': form,
        'hire': hire,
    }

    return render(request, 'accounts/update_hire.html', context)

@login_required(login_url='login')
def delete_hire(request, pk):
    hire = get_object_or_404(Hire, pk=pk)
    hire.delete()
    return redirect('customer_dashboard')



def approved_hire_list(request):
    # Get the current logged-in user (customer)
    customer = request.user
    
    # Retrieve the approved hire requests for the customer
    approved_hires = Hire.objects.filter(customer=customer, is_approved=True)
    
    context = {
        'approved_hires': approved_hires
    }
    
    return render(request, 'accounts/approved_hire_list.html', context)


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


