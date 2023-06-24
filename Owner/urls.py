from django.urls import path
from . import views

urlpatterns = [
    path ('owner_add_car/',views.CreateCar, name='CreateCar'),
    path ('owner_view_cars/',views.owner_car_list, name='viewCars'),

    path('owner_rental_requests/', views.owner_notification, name='owner_notification'),
    path('owner_hiring_history/', views.hiring_history, name='hiring_history'),


    # path ('edit/<str:pk>/',views.updateCar, name='update_car'),
]