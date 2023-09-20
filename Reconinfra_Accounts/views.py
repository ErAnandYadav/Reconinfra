from django.shortcuts import get_list_or_404, get_object_or_404
from django.shortcuts import HttpResponse, render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .helpers import send_forget_password_mail
from django.contrib.auth.models import Group
from Reconinfra_Admin_Panel.models import *
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.conf import settings
from django.db.models import Q
from .models import CustomUser
from .forms import *
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
            aadhar_number = form.cleaned_data.get('aadhar_number')
            pan_number = form.cleaned_data.get('pan_number')
            confirm_password = request.POST.get('confirm_password')
            if CustomUser.objects.filter(aadhar_number=aadhar_number).first():
                form.add_error('aadhar_number', "Aadhar number already exist")
                return render(request, 'app/user-register.html', {'form' : form})
            if CustomUser.objects.filter(pan_number=pan_number).first():
                form.add_error('pan_number', "PAN number already exist")
                return render(request, 'app/user-register.html', {'form' : form})
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
        else:
            form.errors['__all__'] = "Email Already"
            return render(request, 'app/user-register.html', {'form' : form, 'sponsor_id': sponsor_id})
    form = UserRegisterForm()
    return render(request, 'app/user-register.html', {'form' : form, 'sponsor_id': sponsor_id})

def LoginView(request):
    if request.method == 'POST':
        login_identifier = request.POST.get('login_identifier')  # Rename the input field to 'login_identifier'
        password = request.POST.get('password')
        print("xxxxxxxxxxx", login_identifier, password)

        # Check if login_identifier is a valid email
        if '@' in login_identifier:
            user_obj = CustomUser.objects.filter(email=login_identifier.lower(), is_superuser=True).first()
        else:
            user_obj = CustomUser.objects.filter(sponsor_id=login_identifier).first()

        if user_obj:
            user = authenticate(request, email=user_obj.email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome to the Recon Group Mr. {user_obj.first_name} {user_obj.last_name}')
                return HttpResponseRedirect('/app/')
            else:
                messages.info(request, "Credentials do not match!")
        else:
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
    if request.user.is_superuser:
        balance = PlotBooking.objects.all().aggregate(wallet_balance = Sum("down_payment"))
        monthly_business = PlotBooking.objects.filter(created_at__month = timezone.now().month).aggregate(wallet_balance = Sum("down_payment"))
        context['balance'] = balance
        context['monthly_business'] = monthly_business
        context['form'] = form
    else:
        balance = PlotBooking.objects.filter(associate_id=request.user.sponsor_id).aggregate(wallet_balance = Sum("down_payment"))
        monthly_business = PlotBooking.objects.filter(associate_id=request.user.sponsor_id, created_at__month = timezone.now().month).aggregate(wallet_balance = Sum("down_payment"))
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

def ChangeProfilePicture(request):
    if request.method =='POST':
        profile_pic = request.FILES.get('profile_pic')
        print(profile_pic)
        user = CustomUser.objects.get(account_id=request.user.account_id)
        user.profile_pic = profile_pic
        user.save()
        messages.success(request, "Profile picture updated successfully")
        return redirect('/accounts/change-profile-picture/')
    return render(request, "app/change-profile-picture.html")



def MyTeamsView(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/auth-login/')
    teams_list = []
    indirect_teams_count = 0
    team_business = 0
    if request.user.is_superuser:
        teams = CustomUser.objects.filter(is_superuser = True)
        count = teams.count()
        for team in teams:
            indirect_teams = CustomUser.objects.filter(is_superuser = False).exclude(referred_by_id=team.account_id, )
            print(indirect_teams, "87777777777777777777")
            indirect_teams_count += indirect_teams.count()
            teams_business = PlotBooking.objects.all().aggregate(wallet_balance = Sum("down_payment")),
            if teams_business[0]['wallet_balance']:
                team_business += round(teams_business[0]['wallet_balance'])
            data = {
                "account_id": team.account_id,
                "full_name": team.first_name+ ' ' +team.last_name,
                "associate_id":team.sponsor_id,
                "level":team.business_level,
                "total_business": PlotBooking.objects.filter(associate_id = team.sponsor_id).aggregate(wallet_balance = Sum("down_payment")),
                "direct_teams": CustomUser.objects.filter(referred_by_id=team.account_id).count(),
                "indirect_teams_count": indirect_teams_count,
                "teams_business": team_business,
            }
            teams_list.append(data)
    else:
        teams = CustomUser.objects.filter(referred_by=request.user)
        count = teams.count()
        for team in teams:
            indirect_teams = CustomUser.objects.filter(referred_by_id=team.account_id)
            indirect_teams_count += indirect_teams.count()
            teams_business = PlotBooking.objects.filter(associate_id=team.sponsor_id).aggregate(wallet_balance = Sum("down_payment")),
            if teams_business[0]['wallet_balance']:
                team_business += round(teams_business[0]['wallet_balance'])
            data = {
                "account_id": team.account_id,
                "full_name": team.first_name+ ' ' +team.last_name,
                "associate_id":team.sponsor_id,
                "level":team.business_level,
                "total_business": PlotBooking.objects.filter(associate_id = team.sponsor_id).aggregate(wallet_balance = Sum("down_payment")),
                "direct_teams": CustomUser.objects.filter(referred_by_id=team.account_id).count(),
                "indirect_teams_count": indirect_teams_count,
                "teams_business": team_business,
            }
            teams_list.append(data)
  
    return render(request, "app/my-teams.html",{'teams':teams_list, 'count':count})

def TeamDetailsView(request, account_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/auth-login/')
    teams_list = []
    indirect_teams_count = 0
    team_business = 0
    total_business = 0
    direct_teams = 0
    try:
        teams = CustomUser.objects.filter(referred_by_id = account_id)
        for team in teams:
            indirect_user = CustomUser.objects.filter(referred_by_id = team.account_id)
            total_business = PlotBooking.objects.filter(associate_id=team.sponsor_id).aggregate(wallet_balance = Sum("down_payment"))['wallet_balance']
            direct_teams = CustomUser.objects.filter(referred_by_id = team.account_id).count()
            for x in indirect_user:
                ind_usr = CustomUser.objects.filter(referred_by_id = x.account_id).count()
                indirect_teams_count +=ind_usr
                indirect_team_business = PlotBooking.objects.filter(associate_id=x.sponsor_id).aggregate(wallet_balance = Sum("down_payment"))['wallet_balance']
                if indirect_team_business is not None:
                    team_business += indirect_team_business
            data = {
                "account_id": team.account_id,
                "full_name": team.first_name+ ' ' +team.last_name,
                "associate_id":team.sponsor_id,
                "level":team.business_level,
                "total_business": total_business,
                "direct_teams": direct_teams,
                "indirect_teams_count": indirect_teams_count,
                "teams_business": team_business,
            }
            teams_list.append(data)
    except Exception as e:
        print(e)
    return render(request, "app/team-details.html",{'teams':teams_list})


def SearchTeamsView(request):
    teams_list = []
    query = request.GET.get('query')
    print(query)
    teams = CustomUser.objects.filter(Q(first_name__icontains=query) | Q(sponsor_id__icontains=query))
    count = CustomUser.objects.filter(Q(first_name__icontains=query) | Q(sponsor_id__icontains=query)).count()
    for team in teams:
        data = {
            "account_id": team.account_id,
            "full_name": team.first_name+ ' ' +team.last_name,
            "associate_id":team.sponsor_id,
            "level":team.business_level,
            "total_business": PlotBooking.objects.filter(associate_id = team.sponsor_id).aggregate(wallet_balance = Sum("down_payment")),
            "total_teams": CustomUser.objects.filter(referred_by_id=team.account_id).count()
        }
        teams_list.append(data)
    
    return render(request, "app/my-teams.html",{'teams':teams_list, 'count':count, 'query':query})






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



# views.py
import pandas as pd
from django.http import HttpResponse
from django.contrib.auth.models import User

def export_users_to_csv(request):
    # Query all user objects from the database
    users = CustomUser.objects.all()

    # Create a Pandas DataFrame with user data and column names
    user_data = {
        'account_id': [user.account_id for user in users],
        'email': [user.email for user in users],
        'first_name': [user.first_name for user in users],
        'last_name': [user.last_name for user in users],
        'phone_number': [user.phone_number for user in users],
        'profile_pic': [user.profile_pic for user in users],
        'is_superuser': [user.is_superuser for user in users],
        'is_staff': [user.is_staff for user in users],
        'is_active': [user.is_active for user in users],
        'is_admin': [user.is_admin for user in users],
        'is_facilitator': [user.is_facilitator for user in users],
        'is_accountent': [user.is_accountent for user in users],
        'aadhar_number': [user.aadhar_number for user in users],
        'aadhar_front': [user.aadhar_front for user in users],
        'aadhar_back': [user.aadhar_back for user in users],
        'pan_number': [user.pan_number for user in users],
        'pan_front': [user.pan_front for user in users],
        'pan_back': [user.pan_back for user in users],
        'account_holder_name': [user.account_holder_name for user in users],
        'account_number': [user.account_number for user in users],
        'account_type': [user.account_type for user in users],
        'ifsc_code': [user.ifsc_code for user in users],
        'bank_name': [user.bank_name for user in users],
        'branch_name': [user.branch_name for user in users],
        'country': [user.country for user in users],
        'state': [user.state for user in users],
        'city': [user.city for user in users],
        'address': [user.address for user in users],
        'referred_by': [user.referred_by for user in users],
        'sponsor_id': [user.sponsor_id for user in users],
        'is_wallet_active': [user.is_wallet_active for user in users],
        'business_level': [user.business_level for user in users],
        'forget_password_token': [user.forget_password_token for user in users],
        'password': [user.password for user in users],
    }
    df = pd.DataFrame(user_data)

    # Create a response with a CSV attachment
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    # Write the DataFrame to the response as a CSV file
    df.to_csv(response, index=False)

    return response
