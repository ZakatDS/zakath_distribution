from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# from .utils import generate_otp, verify_otp
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from geopy.geocoders import Photon


from .models import *

# Create your views here.

# home page ---------------------------------------------------------
def home(req):
    context = {}
    return render(req, 'home.html', context)

# Signin Signout Signup ---------------------------------------------
def signin(req, next="home"):
    if req.method == 'POST':
        email = req.POST.get('email').lower()
        password = req.POST.get('password')

        try:
            user = User.objects.get(email = email)
        except:
            messages.error(req, 'Account with the corresponding email does not exist.', )
            return redirect('signin')
            # return HttpResponse('Account with the corresponding email does not exist')
        
        user = User.objects.get(email = email)
        
        user = authenticate(req, email = email, password = password)

        if user is not None:
            login(req, user)

            if user.is_email_verified:
                if user.is_verified:
                    try:
                        return redirect(next)
                    except:
                        return redirect('home')
                try:
                    return redirect(next)
                except:
                    return redirect('home')
            else:
                return redirect('verify-email')

        else:
                messages.error(req, "Username or Password does not match...")
                return redirect('signin')


        
    context = {}
    return render(req, 'zakath/login.html', context)

def signout(req):
    logout(req)
    return redirect('signin')

def register(req):

    # mahals = Mahal.objects.all()

    if req.method == 'POST':
        email = req.POST.get('email').lower()
        name = req.POST.get('name')
        address = req.POST.get('address')
        
        if address is None or address == '':
            address = ""

        phone_code = req.POST.get('phone_code')
        phone_no = req.POST.get('phone')

        if phone_code is not None or phone_code != '':
            if '+' in phone_code:
                phone_no = phone_code + phone_no
            else:
                phone_code = '+' + phone_code
                phone_no = phone_code + phone_no
        else: 
            phone_no = phone_no


        if req.POST.get('status') == 'is_donor':
            is_donor = True
            is_receiver = False
        else:
            is_donor = False 
            is_receiver = True 


        password = req.POST.get('password')
        password2 = req.POST.get('password2')


        if User.objects.filter(email=email).exists():
            messages.error(req, "This email already exists. Try logging in.")
            return redirect('signin')
        else:
            if password == password2:
                # mahal, created = Mahal.objects.get_or_create(name=mahal_name)

                user = User.objects.create(email = email, name = name, address = address, is_verified = True, is_donor = is_donor, is_receiver = is_receiver)
                try:
                    user.phone_no = phone_no
                except:
                    pass

                user.set_password(password)
                user.save()
                login(req, user)

                if is_donor:
                    user.is_verified = True
                    user.save()
                
                else:
                    user.is_verified = False
                    user.save()

                user.save()

                return redirect('verify-email')
            else:
                messages.error(req, "Passwords do not match")
                return redirect('register')



    context = {
    }
    return render(req, 'zakath/register.html', context)



# email
def verify_email(request):
    if request.method == "POST":
        if request.user.is_email_verified != True:
            current_site = get_current_site(request)
            user = request.user
            email = request.user.email
            subject = "Verify Email"
            message = render_to_string('zakath/verify_email_message.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            return redirect('verify-email-done')
        else:
            return redirect('signup')

    return render(request, 'zakath/verify_email.html')

def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('verify-email-complete')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'zakath/verify_email_confirm.html')

def verify_email_done(request):
    if request.user.is_email_verified:
        messages.success(request, 'Your email has been verified. Now add your location after logging in.')
        return redirect('add_location')
    
    return render(request, 'zakath/verify_email_done.html')

def verify_email_complete(request):
    messages.success(request, 'Your email has been verified. Now add your location.')
    return redirect('add_location')


def verify_email_message(req):
    return render(req, 'zakath/verify_email_message_test.html')    
    
# email end

@login_required(login_url= '/signin/bankData')      
def bankData(req):

    if req.method == 'POST':
        bank_name = req.POST.get('bankName')
        acc_no = req.POST.get('accountNumber')
        IFC_code = req.POST.get('ifscCode')
        UPI_id = req.POST.get('UPI_ID')

        req.user.bank_name = bank_name
        req.user.acc_no = acc_no
        req.user.IFSC_code = IFC_code
        req.user.UPI_ID = UPI_id

        user = req.user

        user.save()

        return redirect('home')
            
    context = {}
    return render(req, 'zakath/bankData.html', context)

@login_required(login_url= '/signin/dashboard')
def dashboard (req):
    if req.user.is_email_verified:
        user = req.user
        
        recievers = User.objects.filter(is_receiver = True, place=req.user.place)

        if req.user in recievers:
            recievers = recievers.exclude(id = req.user.id)


        context = {
            'data': recievers,
        }

        return render(req, 'zakath/dashboard.html', context)
    else:
        return redirect('verify-email')



@login_required(login_url= '/signin')
def donate(req, user_id):

    try:
        reciever =  User.objects.get(pk=user_id)
        context = {
            'reciever': reciever,
        }
        return render(req, 'zakath/donate.html', context)
    except: 
        context = {}
        return render(req, 'zakath/donate.html', context)
        


# User Approval (admi only)-------------------------------------------------------------
@login_required(login_url= '/signin/user_approval')
def user_approval(req):
    if req.user.is_superuser or req.user.is_qazi or req.user.is_qazi:
        non_verified_users = User.objects.filter(is_email_verified = True, is_verified = False)

        context = {
            'non_verified_users' : non_verified_users
        }
        return render(req, 'zakath/admin/user_approval.html', context)
    else:
        return HttpResponse('Your Cant Enter to This Page')


@login_required(login_url= '/signin/user_approval')
def verify(req, pk):
    if req.user.is_superuser:
        user = User.objects.get(id = pk)
        user.is_verified = True
        user.save()
        return redirect('user_approval')
    else:
        raise ValueError("You need to be an admin in order to perform this action.")

@login_required(login_url= 'signin/user_approval')
def delete (req, pk):
    if req.user.is_superuser:
        user = User.objects.get(id = pk)
        user.delete()
        return redirect('user_approval')
    else:
        raise ValueError("You need to be an admin in order to perform this action.")

# calculator --------------------------------------------------------------
def calculator(req):
    context = {
    }
    return render(req, 'zakath/calculator/calculator.html', context)

@login_required(login_url='signin/calculator')
def save_calculation(req):

    if req.method == 'POST':
        items = {
            'Gold': req.POST.get('Gold'),
            'Silver': req.POST.get('Silver'),
            'Cash': req.POST.get('Cash'),
            # 'Given': req.POST.get('Given'),
            'goods': req.POST.get('goods'),
            'AI': req.POST.get('AI'),
            'NI': req.POST.get('NI'),
            'tresure': req.POST.get('tresure'),
            'zakath': req.POST.get('zakath'),
            'asset': req.POST.get('asset'),
        }

        for key, item in items.items():
            if item == '' or item is None:
                items[key] = 0
            else:
                items[key] = item
                print(items[key], ' ', type(items[key]))

        calculation = Calculator.objects.create(user = req.user,
         AI= items['AI'], 
         NI = items['NI'], 
         tresure = items['tresure'], 
         Gold = items['Gold'], 
         Silver = items['Silver'], 
         Cash = items['Cash'], 
        #  Given = items['Given'], 
         goods = items['goods'], 
         zakath = items['zakath'], 
         asset = items['asset']
        )
        
        calculation.save()

    return redirect('calculator')

@login_required(login_url='signin/livestock_calc')
def livestock_calc(req):

    context = {}
    return render(req, 'zakath/calculator/livestock.html', context)

@login_required(login_url='signin/livestock_calc')
def save_livestock_calc(req): 
    
    if req.method == 'POST':
        items = {
            'goat': req.POST.get('goat'),
            'goat_zakath': req.POST.get('goat_zakath'),

            'cow': req.POST.get('cow'),
            'cow_zakath': req.POST.get('cow_zakath'),

            'camel': req.POST.get('camel'),
            'camel_zakath': req.POST.get('camel_zakath'),

        }

        for key, item in items.items():
            if item == '' or item is None:
                items[key] = 0
            else:
                items[key] = item
                print(items[key], ' ', type(items[key]))

        calculation = Livestock_calculator.objects.create(user = req.user,
         goat= items['goat'], 
         goat_zakth= items['goat_zakath'], 

         cow = items['cow'], 
         cow_zakth = items['cow_zakath'], 

         camel = items['camel'], 
         camel_zakth = items['camel_zakath'], 

        )
        calculation.save()
        return redirect ('livestock_calc')

#map --------
@login_required(login_url='signin/add_location')
def add_location(req):
    
    context = {
        'has_location': False
    }
    return render(req, 'map/map.html')


@login_required(login_url='signin/add_location')
def process_location(req):
    import urllib.request, json


    if req.method == 'POST':
        lat = req.POST.get('lat')
        lng = req.POST.get('lng')
        save_address = req.POST.get('save_address')

        url = f'https://nominatim.openstreetmap.org/reverse.php?lat={lat}&lon={lng}&zoom=18&format=geojson&accept-language=en-US'

        address_str = ""

        with urllib.request.urlopen(url) as url:
            address = json.load(url)
            
        try:
            address = address['features'][0]['properties']['address']
        except:
            address = ''

        if save_address == 'on': 
            if address != '' or address != None:
                try:
                    for key, value in address.items():
                        address_str += f"{value}, "
                except:
                    pass


        # req.user.country = address['country']
        try:
            req.user.place = address['county']
        except:
            try:
                req.user.place = address['state_district']
            except:
                try:
                    req.user.place = address['state']
                except:
                    req.user.place = address['country']

        req.user.address = address_str
        req.user.latitude = lat
        req.user.longitude = lng
        req.user.save()
        
    return redirect('home')

