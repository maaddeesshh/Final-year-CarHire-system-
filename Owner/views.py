from django.shortcuts import render , redirect ,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CarForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from Hire.models  import Hire
# Create your views here
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import *
from Owner.models import Car
from django.shortcuts import render, redirect

from django.contrib import messages

# Create your views here.
 
def CreateCar(request):
    form = CarForm()
    if request.method == 'POST':
            form = CarForm(request.POST,request.FILES)
            if form.is_valid():
                car= form.save(commit=False)
                car.owner = request.user
                car.save()
                return HttpResponseRedirect(reverse('owner_dashboard'))
                # return redirect ('owner_dashboard')
            
    context= {'form':form}
    return render(request, 'Owner/createcar.html', context)




@login_required(login_url='login')
def owner_car_list(request):
    user = request.user
    cars = Car.objects.filter(owner=user)

    context = {
        'cars': cars
    }

    return render(request, 'Owner/owner_car_list.html', context)

@login_required(login_url='login')
def hiring_history(request):
    user = request.user
    cars = Car.objects.filter(owner=user)
    hires = Hire.objects.filter(car__in=cars)
    return render(request, 'Owner/hiring_history.html', {'hires': hires})




def owner_notification(request):
    user = request.user
    owned_cars = Car.objects.filter(owner=user)
    pending_hires = Hire.objects.filter(car__in=owned_cars, is_approved=False, is_rejected=False).order_by('-id')

    notification_count = pending_hires.count()
  

    return render(request, 'Owner/owner_notification.html', {'pending_hires': pending_hires, 'notification_count': notification_count})





def approve_hire(request, hire_id):
    hire = get_object_or_404(Hire, pk=hire_id)
    hire.is_approved = True
    hire.is_rejected = False
    hire.save()
     # Send the hire approval email
    send_hire_approval_email(request, hire_id)
    return redirect('owner_dashboard')  # Replace with the appropriate URL for the hire list

def reject_hire(request, hire_id):
    hire = get_object_or_404(Hire, pk=hire_id)
    hire.is_approved = False
    hire.is_rejected = True
    hire.save()
    return redirect('owner_dashboard')  # Replace with the appropriate URL for the hire list


def approved(request):
    # Retrieve all approved hire requests
    approved_hires = Hire.objects.filter(is_approved=True)

    # Pass the approved hires to the template context
    context = {
        'approved_hires': approved_hires
    }

    return render(request, 'Owner/approved.html', context)




def send_hire_approval_email(request, hire_id):
    # Retrieve the Hire object
    hire = Hire.objects.get(id=hire_id)
    cars = Car.objects.all()

    # Check if the hire is approved
    if hire.is_approved:
        # Get the customer's email and other details
        customer_email = hire.customer.email
        customer_name = hire.customer.username
        driver_name = cars.owner.username

        car = cars.reg_no
        hire_schedule = hire.start_date
        hire_end = hire.end_date

        # Prepare the email content
        subject = 'Hire Request Approved'
        html_message = render_to_string('Owner/approval_notification.html', {
            'customer_name': customer_name,
            'hire_start_date': hire_schedule,
            'hire_end': hire_end,
            'driver_name': driver_name,
            'car': car,
        })
        plain_message = strip_tags(html_message)

        # Send the email
        # send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [customer_email], html_message=html_message)
        send_mail(subject, plain_message, settings.HIRE_APPROVAL_EMAIL_HOST_USER, [customer_email], html_message=html_message)



        # Add any additional logic or redirect the user to an appropriate page
        return HttpResponseRedirect(reverse('customer_dashboard'))
    else:
        # Handle the case where the hire request is not approved
        # Add appropriate logic or redirect the user to an appropriate page
        return HttpResponseRedirect(reverse('customer_dashboard'))
