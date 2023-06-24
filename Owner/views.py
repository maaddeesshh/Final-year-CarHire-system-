from django.shortcuts import render , redirect ,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CarForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from Hire.models  import Hire

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




def approve_hire(request, pk):
    hire = get_object_or_404(Hire, pk=pk)
    hire.is_approved = True
    hire.save()
    # You can add a success message to the session variable
    request.session['notification'] = 'Hire request approved successfully.'
    return redirect('owner_dashboard')

def reject_hire(request, pk):
    hire = get_object_or_404(Hire, pk=pk)
    hire.is_rejected = True
    hire.save()
    # You can add a success message to the session variable
    request.session['notification'] = 'Hire request rejected.'
    return redirect('owner_dashboard')

