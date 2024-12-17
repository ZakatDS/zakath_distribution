from django.db import models 
 
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
# from django.contrib.
from .managers import UserManager
# Create your models here. 

# class Mahal (models.Model): 
#     name = models.CharField(max_length=150) 

#     def __str__(self): 
#         return self.name

class User(AbstractBaseUser):
    email = models.EmailField(_("Email Address"), blank=False, unique=True, null=False)
    name = models.CharField(_("Full Name"), blank=False, max_length=250)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    place = models.CharField(blank=True)

    address = models.TextField(blank=True)
    phone_no = PhoneNumberField(blank=True)
    date_joined = models.DateField(_("Date Joined"), auto_now_add=True)
    last_login = models.DateField(_("Last Login"), auto_now=True)

    is_receiver = models.BooleanField(blank=False)
    is_donor = models.BooleanField(blank=False)
    # is_qazi = models.BooleanField(default=False)


    is_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)



    bank_name = models.CharField(max_length=50, null=True, blank=True)
    acc_no = models.CharField(max_length=50, null=True, blank=True)
    IFSC_code = models.CharField(max_length=50, null=True, blank=True)
    UPI_ID = models.CharField(max_length=50, null=True, blank=True)

    USERNAME_FIELD = 'email'


    REQUIRED_FIELDS = [
        'name'
    ]
    
    objects = UserManager()


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        if self.is_receiver == True and self.is_donor == True:
            raise ValueError("Both is_receiver and is_donor is set to True.")

        return self.email

 
class Calculator (models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    Gold = models.IntegerField(null=True, blank=True, default=0)
    Silver = models.IntegerField(null=True, blank=True, default=0)
    Cash = models.IntegerField(null=True, blank=True, default=0)
    goods = models.IntegerField(null=True, blank=True, default=0)
    # Given = models.IntegerField(null=True, blank=True, default=0)
    AI = models.IntegerField(null=True, blank=True, default=0)
    NI = models.IntegerField(null=True, blank=True, default=0)
    tresure = models.IntegerField(null=True, blank=True, default=0)

    zakath = models.FloatField(null=True, blank=True, default=0)
    asset = models.FloatField(null=True, blank=True, default=0)
    
    date = models.DateField(_("Date"), auto_now=True, auto_now_add=False, null=True)

    def __str__(self):
        return self.user.name 
 

class Livestock_calculator (models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    goat = models.IntegerField(null=True, blank=True, default=0)
    goat_zakath = models.CharField(null=True, blank=True, default=0)

    camel = models.IntegerField(null=True, blank=True, default=0)
    camel_zakath = models.CharField(null=True, blank=True, default=0)

    cow = models.IntegerField(null=True, blank=True, default=0)
    cow_zakath = models.CharField(null=True, blank=True, default=0)
    
    date = models.DateField(_("Date"), auto_now=True, auto_now_add=False, null=True)

    def __str__(self):
        return self.user.name 


class TempUrl(models.Model):
    url = models.URLField(blank=False, unique=True, null=False)
    expiry = models.DateTimeField(auto_now_add=True)

    def get_time(sec=0, hour=0, day=0, month=0, year=0):
        pass

    def __str__(self):
        return self.url