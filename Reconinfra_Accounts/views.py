from django.shortcuts import get_list_or_404, get_object_or_404
from django.shortcuts import HttpResponse, render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import CustomUser
from Reconinfra_Admin_Panel.models import *
from django.db.models import Sum
from django.utils import timezone
from .forms import *
from .helpers import send_forget_password_mail
import random,math
import uuid

def UserRegister(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            sponsor_id = request.POST.get('sp_id')
            print(sponsor_id)
            first_name = form.cleaned_data.get("first_name")
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password != confirm_password:
                form.add_error('password', "Password and Confirm Password does not Match")
                return render(request, 'app/user-register.html', {'form' : form})
            if sponsor_id:
                sponsor_obj = CustomUser.objects.filter(sponsor_id = sponsor_id).exists()
                if sponsor_obj:
                    user_obj = CustomUser.objects.get(sponsor_id = sponsor_id)
                    print(user_obj, "54444444444444444444444")
                    user = form.save()
                    user.set_password(user.password)
                    user.referred_by_id = user_obj.account_id
                    user.save()
                    subject = 'Welcome to Recon Group'
                    message = f'Dear {user.first_name} {user.last_name}, Thank You For Registering in Recon Group. Your Login id: {user.sponsor_id} and Password : {password}'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                    messages.success(request, 'Account Created Successfully! Please Check Mail')
                    return redirect('/accounts/auth-login/')
                form.add_error('sponsor_id', "Invalid Sponsor ID. Please Enter Valid Sponsor ID!")
                return render(request, 'app/user-register.html', {'form' : form})
            form.add_error('sponsor_id', "Please enter sponsor id")
            return render(request, 'app/user-register.html', {'form' : form})
            # user = form.save()
            # user.set_password(user.password)
            # # user.referred_by_id = sp_id
            # user.save()
            # subject = 'Welcome to Recon Group'
            # message = f'Dear {user.first_name} {user.last_name}, Thank You For Registering in Recon Group. Your Login ID : {user.email} and Password : {password}'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [user.email, ]
            # send_mail( subject, message, email_from, recipient_list )
            # messages.success(request, 'Account Created Successfully! Please Check Mail')
            # return redirect('/accounts/auth-login/')
        else:
            form.errors['__all__'] = "Email Already"
            return render(request, 'app/user-register.html', {'form' : form})
    else:
        form = UserRegisterForm()
        return render(request, 'app/user-register.html', {'form' : form})

def ReferralLinkView(request, sponsor_id):
    if request.method =='POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password != confirm_password:
                form.add_error('password', "Password and Confirm Password does not Match")
                return render(request, 'app/user-register.html', {'form' : form})
            if sponsor_id:
                sponsor_obj = CustomUser.objects.filter(sponsor_id = sponsor_id).exists()
                if sponsor_obj:
                    user_obj = CustomUser.objects.get(sponsor_id = sponsor_id)
                    user = form.save()
                    user.set_password(user.password)
                    user.referred_by_id = user_obj.account_id
                    user.save()
                    subject = 'Welcome to Recon Group'
                    message = f'Dear {user.first_name} {user.last_name}, Thank You For Registering in Recon Group. Your Login id : {user.sponsor_id} and Password : {password}'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user.email, ]
                    send_mail(subject, message, email_from, recipient_list )
                    messages.success(request, 'Account Created Successfully! Please Check Mail')
                    return redirect('/accounts/auth-login/')
                form.add_error('sponsor_id', "Invalid Sponsor ID. Please Enter Valid Sponsor ID!")
                return render(request, 'app/user-register.html', {'form' : form})
            form.add_error('sponsor_id', "Please enter sponsor id")
            return render(request, 'app/user-register.html', {'form' : form})
            # user = form.save()
            # user.set_password(user.password)
            # # user.referred_by_id = sp_id
            # user.save()
            # subject = 'Welcome to Recon Group'
            # message = f'Dear {user.first_name} {user.last_name}, Thank You For Registering in Recon Group. Your Login ID  {user.email} and Password : {password}'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [user.email, ]
            # send_mail( subject, message, email_from, recipient_list )
            # messages.success(request, 'Account Created Successfully! Please Check Mail')
            # return redirect('/accounts/auth-login/')
        else:
            form.errors['__all__'] = "Email Already"
            return render(request, 'app/user-register.html', {'form' : form, 'sponsor_id': sponsor_id})
    form = UserRegisterForm()
    return render(request, 'app/user-register.html', {'form' : form, 'sponsor_id': sponsor_id})

def LoginView(request):
    if request.method =='POST':
        sponsor_id = request.POST.get('sponsor_id')
        password = request.POST.get('password')
        print("xxxxxxxxxxx", sponsor_id, password)
        user_obj = CustomUser.objects.filter(sponsor_id=sponsor_id).first()
        if user_obj:
            user = authenticate(request, email=user_obj.email, password=password)
            print(user)
            if user is not None:
                login(request , user)
                messages.success(request, f'Welcome to the Recon Group Mr. {user_obj.first_name} {user_obj.last_name}')
                return HttpResponseRedirect('/app/')
            # messages.info(request, "Your Have Not Permission!")
            # return redirect('/accounts/auth-login/')
            else:
                messages.info(request, "Credential Are Not Match!")
                return redirect('/accounts/auth-login/')
        messages.info(request, "Invalid username or password. Please check your credentials and try again.")
        return redirect('/accounts/auth-login/')
    return render(request, 'app/sign-in.html')

def LogoutView(request):
    try:
        logout(request)
        messages.info(request, "Logout Successfully!")
        return redirect('/accounts/auth-login/')
    except Exception as e:
        print(e)


def Profile(request, id):
    context = {}
    instance = get_object_or_404(CustomUser, account_id=id)
    form = UserUpdateForm(request.POST or None,request.FILES or None, instance=instance)
    if form.is_valid():
        profile_pic = form.cleaned_data.get('profile_pic')
        print(profile_pic)
        form.save()
        return redirect('/app/')
    balance = Wallet.objects.filter(agent_id = request.user.account_id).aggregate(wallet_balance = Sum("balance"))
    monthly_business = Wallet.objects.filter(agent_id = request.user.account_id, timestamp__month = timezone.now().month).aggregate(wallet_balance = Sum("balance"))
    context['balance'] = balance
    context['monthly_business'] = monthly_business
    context['form'] = form
    form.errors['__all__'] = "Something went wrong"
    print(form.errors)
    return render(request, "app/profile.html",context)


def UpdateBankDetails(request):
    context = {}
    try:
        form = UpdateBankDetailsForm()
        context['form'] = form
    except Exception as e:
        print(e)
    return render(request, "app/update-bank-details.html",context)


def MyTeamsView(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/auth-login/')
    context = {}
    try:
        teams = CustomUser.objects.filter(referred_by_id = request.user.account_id)
        context['teams'] = teams
    except Exception as e:
        print(e)
    return render(request, "app/my-teams.html",context)

def ForgetPasswordView(request):
    try:
        if request.method =='POST':
            email = request.POST.get('email')
            if not CustomUser.objects.filter(email=email).first():
                messages.error(request, "User Not Found!")
                return redirect('/accounts/forget-password/')
            user_obj = CustomUser.objects.get(email=email)
            token = str(uuid.uuid4())
            user_obj.forget_password_token = token
            user_obj.save()
            send_forget_password_mail(user_obj, token)
            messages.info(request, "An Email is sent!")
            return redirect('/accounts/forget-password/')
    except Exception as e:
        print(e)
    return render(request, "app/forget-password.html")

def ChangePasswordView(request, token):
    context = {}
    try:
        user_obj = CustomUser.objects.filter(forget_password_token = token).first()
        if request.method =='POST':
            password = request.POST.get('new-password')
            confirm_password = request.POST.get('confirm-password')
            user_id = request.POST.get('user_id')
            if user_id is None:
                messages.error(request, "User not Found!")
                return redirect(f'/accounts/change-password/{token}/')
            if password !=confirm_password:
                messages.error(request, "New Password and Confirm Password are Not Same!")
                return redirect(f'/accounts/change-password/{token}/')
            usr = CustomUser.objects.get(account_id=user_id)
            usr.set_password(password)
            usr.save()
            messages.success(request, "Your Password Change Successfully!")
            return redirect(f'/accounts/auth-login/')
        context = {"user_id" : user_obj.account_id}
       
    except Exception as e:
        print(e)
    return render(request, "app/change-password.html", context)

def CreateGroupView(request):
    context = {}
    try:
        if request.method =='POST':
            form = GroupForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Group Created Successfully")
                return redirect('/accounts/group-list/')
            else:
                return render(request, "app/add-group.html", {'form' : form})
        form = GroupForm()
        context['form'] = form
    except Exception as e:
        print(e)
    return render(request, "app/add-group.html", context)

def GroupListView(request):
    context = {}
    groups = Group.objects.all()
    context['groups'] = groups
    return render(request, "app/group-list.html", context)

def AssignGroupView(request):
    context = {}
    try:
        if request.method =='POST':
            form = GroupInitializeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Group Initialize Successfully")
                return redirect('/accounts/assign-group/')
            else:
                return render(request, "app//initialize-group.html", {'form' : form})
        form = GroupInitializeForm()
        context['form'] = form
    except Exception as e:
        print(e)
    return render(request, "app/initialize-group.html",context)

def InitializeGroupListView(request):
    context = {}
    initialize_groups = GroupInitialize.objects.all()
    context['initialize_groups'] = initialize_groups
    return render(request, "app/initialize-group-list.html",context)

def GroupsAgentListView(request, pk):
    context = {}
    agents = GroupInitialize.objects.filter(group_id = pk)
    print(agents)
    context['agents'] = agents
    return render(request, "app/agents-in-group.html", context)

def EditFacilitatorView(request, pk):
    associate = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = UpdateRegisterForm(request.POST, instance=associate)
        if form.is_valid():
            form.save()
            messages.success(request, "Facilitator details updated successfully")
            return redirect('/app/facilitator-list')
    else:
        form = UpdateRegisterForm(instance=associate)

    return render(request, 'app/edit-facilitator.html', {'form': form})


from django.http import JsonResponse
def getAssociateNameBySponsorIdView(request, sponsor_id):
    print(sponsor_id)
    try:
        user = CustomUser.objects.get(sponsor_id=sponsor_id)
        data = {'name': user.first_name+ ' ' +user.last_name}
    except CustomUser.DoesNotExist:
        data = {'name': 'Not found'}

    return JsonResponse(data)
