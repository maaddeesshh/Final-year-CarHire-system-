from django.urls import path
from . import views
from .views import send_hire_approval_email

urlpatterns = [
    path ('owner_add_car/',views.CreateCar, name='CreateCar'),
    path ('owner_view_cars/',views.owner_car_list, name='viewCars'),

    path('owner_rental_requests/', views.owner_notification, name='owner_notification'),
    path('owner_rental_requests_approve/<int:hire_id>/', views.approve_hire, name='approve_hire'),
    path('owner_rental_requests_reject/<int:hire_id>/', views.reject_hire, name='reject_hire'),
    path('owner_approved_requests/', views.approved, name='approved'),
    path('owner_hiring_history/', views.hiring_history, name='hiring_history'),
    path('send_hire_approval_email/<int:hire_id>/', views.send_hire_approval_email, name='send_hire_approval_email'),



    # path ('edit/<str:pk>/',views.updateCar, name='update_car'),
]