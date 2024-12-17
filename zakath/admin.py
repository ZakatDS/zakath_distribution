from django.contrib import admin

from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import PermissionsMixin, Group



# Register your models here.


class CustomUserAdmin(UserAdmin,):
    ordering = ('-date_joined',)
    # Define the list display fields for the admin list view
    list_display = ('email', 'name', 'phone_no', 'date_joined', 'is_verified', 'is_active', 'is_staff', 'is_superuser')

    # Define filters for the admin panel (if needed)
    list_filter = ('is_active', 'is_verified', 'is_staff', 'is_donor', 'is_receiver')

    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'name', 'password1', 'password2', 'is_receiver', 'is_donor'),
    }),
    )
    # Organize fields in the form layout
    fieldsets = (
        (None, {
            'fields': ('id', 'email', 'name', 'phone_no', 'password')
        }),
        ('Admin Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser')
        }),
        ('Verification',{
            'fields': ('is_verified', 'is_email_verified', 'is_mobile_verified',)
        }),
        ('Other Permissions', {
            'fields': ('is_receiver', 'is_donor')
        }),
        ('Dates', {
            'fields': ('date_joined', 'last_login')
        }),
        ('Additional Info', {
            'fields': ('address', 'latitude', 'longitude', 'place')
        }),
        ('Bank Data', {
            'fields': ('bank_name', 'acc_no', 'IFSC_code', 'UPI_ID')
        }),
    )

    # Make fields like 'email' and 'phone_no' readonly in the admin if desired
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    filter_vertical = ()



admin.site.register(User, CustomUserAdmin)
# admin.site.register(Mahal)
# admin.site.register(Zakath_type)
admin.site.register(Calculator)
