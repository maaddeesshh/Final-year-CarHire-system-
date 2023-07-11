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
from django.shortcuts import render
from django.db.models import Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from Hire.models import Hire
from datetime import date
from datetime import timedelta
from django.contrib.auth import get_user_model
from datetime import date
from accounts.models import *
from Hire.models import *
from django.template import loader
from django.db.models import Avg, Count
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from django.http import HttpResponse



def LoginPage(request):
    page = 'login'
    msg = None
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            msg = 'User does not exist'
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard
            
        elif user is not None and user.groups.filter(name='customer').exists():
            login(request, user)
            return redirect('customer_dashboard')
            
        elif user is not None and user.groups.filter(name='owner').exists():
            login(request, user)
            return redirect('owner_dashboard')
          
        else:
            msg = 'Username or password is incorrect'
    
    context = {'msg': msg, 'page': page}
    return render(request, 'accounts/login_register.html', context)


def generate_pdf(html):
    # Create a PDF generator
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Generate PDF using HTML content
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')

    return response

def approved_report(request):
    # Get all approved hire requests
    approved_hires = Hire.objects.filter(is_approved=True)
    logo_path = 'images/logo.svg'
     # Render the HTML template with the approved hire report data
    template = get_template('accounts/approved_report.html')
    html = template.render({'approved_hires': approved_hires, 'logo_path':logo_path}, request)

    # Generate and return the PDF report using ReportLab
    return generate_pdf(html)

    # Render the template with the approved hire report data
    # return render(request, 'accounts/approved_report.html', {'approved_hires': approved_hires})


def rejected_report(request):
    # Get all rejected hire requests
    rejected_hires = Hire.objects.filter(is_rejected=True)
     # Render the HTML template with the rejected hire report data
    template = get_template('accounts/rejected_report.html')
    html = template.render({'rejected_hires': rejected_hires}, request)

    # Generate and return the PDF report using ReportLab
    return generate_pdf(html)

    # Render the template with the rejected hire report data
    # return render(request, 'accounts/rejected_report.html', {'rejected_hires': rejected_hires})
   


def review_report(request):
    # Get all reviews
    reviews = Review.objects.all()

    # Render the HTML template with the review report data
    template = get_template('accounts/review_report.html')
    html = template.render({'reviews': reviews}, request)

    # Generate and return the PDF report using ReportLab
    return generate_pdf(html)

    # Render the template with the review report data
    # return render(request, 'accounts/review_report.html', {'reviews': reviews})

def summary(request):
    user_count = User.objects.count()
    car_count = Car.objects.count()
    hire_count = Hire.objects.count()
    review_count = Review.objects.count()
      # Render the HTML template with the summary report data
    template = get_template('accounts/summary.html')
    html = template.render({
        'user_count': user_count,
        'car_count': car_count,
        'hire_count': hire_count,
        'review_count': review_count
    }, request)

    # Generate and return the PDF report using ReportLab
    return generate_pdf(html)



def CustomAdminDashboard(request):
   return render(request, 'accounts/admin.html')
def filter(request):
     # Filter criteria
    approved_hires = Hire.objects.filter(is_approved=True).count()
    rejected_hires = Hire.objects.filter(is_rejected=True).count()
    customer_users = User.objects.filter(groups__name='customer').count()
    owner_users = User.objects.filter(groups__name='owner').count()
    car_owners = User.objects.filter(groups__name='owner').annotate(num_cars=Count('car')).values('username', 'num_cars')
    reviews_0_to_5 = Review.objects.filter(rate__range=(0, 5)).count()
    reviews_5_to_10 = Review.objects.filter(rate__range=(5, 10)).count()

     # Render the HTML template with the report data
    template = get_template('accounts/filter.html')
    html = template.render({
        'approved_hires': approved_hires,
        'rejected_hires': rejected_hires,
        'customer_users': customer_users,
        'owner_users': owner_users,
        'car_owners': car_owners,
        'reviews_0_to_5': reviews_0_to_5,
        'reviews_5_to_10': reviews_5_to_10
    }, request)

    # Generate and return the PDF report using ReportLab
    return generate_pdf(html)



def customer_report(request):
    # Get query parameters for filtering
    name = request.GET.get('name')
    email = request.GET.get('email')
    registration_date = request.GET.get('registration_date')

    # Filter customers based on query parameters
    customers = User.objects.filter(groups__name='customer')
    if name:
        customers = customers.filter(name__icontains=name)
    if email:
        customers = customers.filter(email__icontains=email)
    if registration_date:
        customers = customers.filter(date_joined=registration_date)

    # Calculate total number of hires for each customer
    customers_with_hires = customers.annotate(total_hires=models.Count('hire'))

     # Render the HTML template with the customer report data
    template = get_template('accounts/customer_report.html')
    html = template.render({'customers': customers_with_hires}, request)

    # Generate and return the PDF report using ReportLab
    return generate_pdf(html)





def owner_report(request):
    # Get query parameters for filtering
    name = request.GET.get('name')
    email = request.GET.get('email')
    registration_date = request.GET.get('registration_date')

    # Filter owners based on query parameters
    owners = User.objects.filter(groups__name='owner')
    if name:
        owners = owners.filter(name__icontains=name)
    if email:
        owners = owners.filter(email__icontains=email)
    if registration_date:
        owners = owners.filter(date_joined=registration_date)

    # Annotate owners with aggregated hire request data
    owners_with_data = owners.annotate(
        total_cars=Count('car', distinct=True),
        total_hire_requests=Count('car__hire', distinct=True),
        total_approved_requests=Sum('car__hire__is_approved'),
        total_rejected_requests=Sum('car__hire__is_rejected')
    )

     # Render the HTML template with the owner report data
    template = get_template('accounts/owner_report.html')
    html = template.render({'owners': owners_with_data}, request)

    # Generate and return the PDF report using ReportLab
    return generate_pdf(html)

    
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
    hires = Hire.objects.filter(customer=user).order_by('-start_date')
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


# def approved_hire_list(request):
#     customer = request.user
#     approved_hires = Hire.objects.filter(customer=customer, is_approved=True).order_by('-start_date')
    
#     current_date = date.today()

#     hires_with_rating = []
#     for hire in approved_hires:
#         if hire.end_date <= current_date and not Review.objects.filter(customer=customer, owner=hire.car.owner).exists():
#             hire.can_rate = True
#         else:
#             hire.can_rate = False
#         hires_with_rating.append(hire)

#     context = {
#         'approved_hires': hires_with_rating,
#         'current_date': current_date,
#     }
#     return render(request, 'accounts/approved_hire_list.html', context)



def approved_hire_list(request):
    customer = request.user
    approved_hires = Hire.objects.filter(customer=customer, is_approved=True).order_by('-start_date')
    
    current_date = date.today()

    hires_with_rating = []
    for hire in approved_hires:
        if hire.end_date <= current_date and not Review.objects.filter(customer=customer, owner=hire.car.owner).exists():
            hire.can_rate = True
        else:
            hire.can_rate = False
        hires_with_rating.append(hire)

    context = {
        'approved_hires': hires_with_rating,
        'current_date': current_date,
    }
    return render(request, 'accounts/approved_hire_list.html', context)




def Rate(request, owner_id):
    owner = get_user_model().objects.get(id=owner_id)
    user = request.user

    current_date = date.today()  # Get the current date

    approved_hires = Hire.objects.filter(customer=user, is_approved=True).order_by('-start_date')

    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.customer = user  # Set the customer field with the current user
            rate.owner = owner
            rate.save()
            return redirect('customer_dashboard')
    else:
        form = RateForm()

    context = {
        'form': form,
        'owner': owner,
        'current_date': current_date,  # Pass the current date to the template context
        'approved_hires': approved_hires,
    }

    return render(request, 'accounts/rate_owner.html', context)



def owner_rating(request):
    owner = request.user

    # Calculate the overall rating
    overall_rating = Review.objects.filter(owner=owner).aggregate(Avg('rate'))['rate__avg']

    context = {
        'owner': owner,
        'overall_rating': overall_rating,
    }

    return render(request, 'accounts/owner_rating.html', context)






# def view_owner_ratings(request):
#     group_name = 'owner'  # The name of the group for owners
#     owners_group = Group.objects.get(name=group_name)
#     owners = owners_group.user_set.all()
#     owner_ratings = []
#     for owner in owners:
#         overall_rating = Review.objects.filter(owner=owner).aggregate(Avg('rate'))['rate__avg']
#         owner_ratings.append({
#             'owner': owner,
#             'overall_rating': overall_rating,
#         })
#     context = {
#         'owner_ratings': owner_ratings,
#     }
#     return render(request, 'accounts/view_owner_ratings.html', context)
def view_owner_ratings(request):
    group_name = 'owner'  # The name of the group for owners
    owners_group = Group.objects.get(name=group_name)
    owners = owners_group.user_set.annotate(num_cars=Count('car'))
    owner_ratings = []
    for owner in owners:
        overall_rating = Review.objects.filter(owner=owner).aggregate(Avg('rate'))['rate__avg']
        car = Car.objects.filter(owner=owner).first()
        phone_number = car.phone_no if car else None  # Fetch the phone number from the associated Car object
        owner_ratings.append({
            'owner': owner,
            'overall_rating': overall_rating,
            'phone_number': phone_number
            
        })

    context = {
        'owner_ratings': owner_ratings,
    }
    return render(request, 'accounts/view_owner_ratings.html', context)




def location_view(request):
    return render(request, 'accounts/location.html')



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


