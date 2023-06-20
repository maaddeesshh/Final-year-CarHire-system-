from django.shortcuts import render , redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CarForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

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