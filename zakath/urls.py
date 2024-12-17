from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),

# Signin Signout Signup
    path('signin', views.signin, name='signin'),
    path('signin/<str:next>', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('register', views.register, name='register'),
    path('addBankData', views.bankData, name='bankData'),



    path('dashboard', views.dashboard, name='dashboard'),

    path('user_approval', views.user_approval, name='user_approval'),
    path('verify/<str:pk>/', views.verify, name='verify'),
    path('delete/<str:pk>/', views.delete, name='delete'),


    path('donate/<int:user_id>', views.donate, name='donate'),
    path('add_location', views.add_location, name='add_location'),
    path('process_location', views.process_location, name='process_location'),

    # calculations
    path('calculator', views.calculator, name='calculator'),
    path('save_calculation', views.save_calculation, name='save_calculation'),

    path('livestock_calc', views.livestock_calc, name='livestock_calc'),
    path('save_livestock_calc', views.save_livestock_calc, name='save_livestock_calc'),

    # Verification
    path('verify-email/', views.verify_email, name='verify-email'),
    path('verify-email-message/', views.verify_email_message, name='verify-email-message'),
    path('verify-email/done/', views.verify_email_done, name='verify-email-done'),
    path('verify-email-confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify-email-confirm'),
    path('verify-email/complete/', views.verify_email_complete, name='verify-email-complete'),
]
