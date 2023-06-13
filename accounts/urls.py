from django.urls import path
from  django.contrib.auth import views as auth_views
from. import views 



urlpatterns = [

    # path('register_owner/', views.owner_signup, name='register_owner'),
     
    # path('login-customer/', views.customer_login, name='customer-login'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('',views.home,name='home'),
    path('about/',views.AboutUs,name="AboutUs"),
    path('owner/',views.ownerPage,name="owner_dashboard"),
    path('customer/',views.customerPage,name="customer_dashboard"),
    # path('admin/',views.admin_dashboard,name="admin_dashboard"),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_complete"),


   
]