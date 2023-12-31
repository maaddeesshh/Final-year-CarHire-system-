from django.urls import path
from  django.contrib.auth import views as auth_views
from. import views #import  all views which is in our app


#define a list of urls that will navigate user
#add a name value to be dynamic
urlpatterns = [

    # path('register_owner/', views.owner_signup, name='register_owner'),
     
    # path('login-customer/', views.customer_login, name='customer-login'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('',views.home,name='home'),
    path('about/',views.AboutUs,name="AboutUs"), 
    path('contact/',views.Contact,name="contact"),
    path('services/',views.Service,name="Services"), 
    # path('Terms_Of_Use/',views.Terms,name="Terms"),
    
    path('custom_admin_dashboard/',views.CustomAdminDashboard,name="admin_dashboard"),
    path('custom_admin_dashboard_filter/',views.filter,name="filter"),
    path('custom_admin_dashboard_summary/',views.summary,name="summary"),
    path('custom_admin_dashboard_customer-report/', views.customer_report, name='customer_report'),
    path('custom_admin_dashboard_owner-report/', views.owner_report, name='owner_report'),
    path('custom_admin_dashboard_approved-report/', views.approved_report, name='approved_report'),
    path('custom_admin_dashboard_reject-report/', views.rejected_report, name='rejected_report'),
    path('custom_admin_dashboard_review-report/', views.review_report, name='review_report'),
    path('custom_admin_dashboard_filter1/',views.filter1,name="filter1"),
    path('custom_admin_dashboard_summary1/',views.summary1,name="summary1"),
    path('custom_admin_dashboard_customer-report1/', views.customer_report1, name='customer_report1'),
    path('custom_admin_dashboard_owner-report1/', views.owner_report1, name='owner_report1'),
    path('custom_admin_dashboard_approved-report1/', views.approved_report1, name='approved_report1'),
    path('custom_admin_dashboard_reject-report1/', views.rejected_report1, name='rejected_report1'),
    path('custom_admin_dashboard_review-report1/', views.review_report1, name='review_report1'),



    path('owner/',views.ownerPage,name="owner_dashboard"),
    path('owner_update/', views.OwnerUpdateProfile, name='owner-update-profile'),
    path('owner_delete/', views.OwnerdeleteAccount, name='owner-delete-profile'),
    path('owner_rating/', views.owner_rating, name='owner-rating'),
    path('customer/',views.customerPage,name="customer_dashboard"),

    path('customer_approved_hire_list/', views.approved_hire_list, name='approved_hire_list'),
    path('customer_approved_hire_list_rate/<int:owner_id>/', views.Rate, name='rate_owner'),
    path('customer_update/', views.UpdateProfile, name='update-profile'),
    path('customer_delete/', views.deleteAccount, name='delete-profile'),
    path ('edit/<str:pk>/',views.updateCar, name='update_car'),
    path ('delete/<str:pk>/',views.deleteCar, name='delete_car'),
    path ('hire/<str:pk>/',views.hire_car,name="hire"),
    path ('hire_success',views.success,name="success"),
  

    path('customer_owner_ratings/', views.view_owner_ratings, name='owner_ratings'),


    path('customer_notification', views.customer_hire_requests, name="request"),
    # path('customer_location/', views.location, name='location'),
    # path('hire_success_update/<str:pk>/', views.update_hire, name='update-hire'),
    path('customer_notification_update_hire/<int:pk>/', views.update_hire, name='update-hire'),
    path('customer_notification_delete_hire/<int:pk>/', views.delete_hire, name='delete-hire'),
    path ('location/',views.location_view,name="map"),
    
    

    # path('hire/update/<int:pk>/', views.update_hire, name='update-hire'),

    # path('admin/',views.admin_dashboard,name="admin_dashboard"),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_complete"),
    path('Terms_Of_Use/',views.Terms,name="Terms"),
   
]