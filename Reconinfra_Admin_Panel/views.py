from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from Reconinfra_Accounts.models import *
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Sum
from django.conf import settings
from .helpers import *
from .forms import *
from .models import *
import random
from django.utils import timezone
# Create your views here.


@login_required(login_url='/accounts/auth-login/')
def Admin_Panel_Home(request):
    context = {}
    current_date = datetime.now()
    # two_days_in_future = current_date + timedelta(days=0)
    # print(two_days_in_future)
    start_date = datetime(current_date.year, current_date.month, 1)

    # Calculate the end date (1st of the next month)
    end_date = start_date + timedelta(days=32)
    end_date = datetime(end_date.year, end_date.month, 1)

    # Build the query to filter records between start_date and end_date
    query = Q(created_at__gte=start_date, created_at__lt=end_date)
    print(query,"578787")
    try:
        if request.user.is_superuser:
            
            balance = PlotBooking.objects.all().aggregate(total_business = Sum("down_payment"))
            monthly_business = PlotBooking.objects.filter(query).aggregate(monthly_business=Sum('down_payment'))['monthly_business']
            context['balance'] = balance
            context['monthly_business'] = monthly_business
            activeUser = CustomUser.objects.filter(is_wallet_active = True).exclude(is_superuser=True).count
            inactiveUser = CustomUser.objects.filter(is_wallet_active = False).exclude(is_superuser=True).count
            context['activeUser'] = activeUser
            context['inactiveUser'] = inactiveUser
            rewards = Reward.objects.all()
        else:
            balance = PlotBooking.objects.filter(associate_id= request.user.sponsor_id).aggregate(total_business = Sum("down_payment")) or 0
            
            print(balance)
            monthly_business = PlotBooking.objects.filter(query).filter(associate_id=request.user.sponsor_id).aggregate(monthly_business=Sum('down_payment'))['monthly_business'] or 0.00
            context['balance'] = balance
            context['monthly_business'] = monthly_business
            activeUser = CustomUser.objects.filter(is_wallet_active = True).exclude(is_superuser=True).count
            inactiveUser = CustomUser.objects.filter(is_wallet_active = False).exclude(is_superuser=True).count
            context['activeUser'] = activeUser
            context['inactiveUser'] = inactiveUser
            
            rewards = Reward.objects.all()
            rewards_list = []
            for x in rewards:
                data = {
                    "title": x.title,
                    "product_type": x.product_type,
                    "description": x.description,
                    "business": x.business,
                    "product_image": x.product_image,
                    "is_lock": x.is_lock,
                    "time_limit": x.time_limit,
                    "progress": round(float(((balance['total_business']) / x.business) * 100),2)
                }
                rewards_list.append(data)
            
            context['rewards'] = rewards_list
    except Exception as e:
        print(e)
    return render(request, 'app/index.html', context)

@login_required(login_url='/accounts/auth-login/')
def AddProperties(request):
    if request.method =='POST':
        try:
            form = AddPropertyForm(request.POST, request.FILES)
            if form.is_valid():
                description = request.POST.get('description')
                plot_types = request.POST.get('plot_types')
                form.save()
                messages.success(request, "Property Added Successfully")
                return redirect('/app/property-list')
            else:
                print(form.errors)
                form.errors['__all__'] = "Somethong wrong"
                return render(request, 'app/add-property.html', {'form':form})
        except Exception as e:
            print(e)
    form = AddPropertyForm()
    return render(request, 'app/add-property.html', {'form':form})


@login_required(login_url='/accounts/auth-login/')
def PropertyList(request):
    context = {}
    try:
        all_properties = Properties.objects.all()
        context['properties'] = all_properties
    except Exception as e:
        print(e)
    return render(request, 'app/property-list.html', context)

@login_required(login_url='/accounts/auth-login/')
def UpdatePropertiesView(request, pk):
    obj = get_object_or_404(Properties, pk=pk) 
    if request.method == 'POST':
        form = AddPropertyForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Plot has been updated successfully!")
            return redirect('/app/property-list')  
    else:
        form = AddPropertyForm(instance=obj) 
    
    return render(request, 'app/edit-property.html', {'form': form})


@login_required(login_url='/accounts/auth-login/')
def DeletePlotView(request, pk):
    try:
        plotObject = get_object_or_404(Properties, id = pk)
        plotObject.delete()
        return redirect('/app/property-list')
    except Exception as e:
        messages.error(request, "You can not delete this plot")
        return redirect('/app/property-list')

@login_required(login_url='/accounts/auth-login/')
def AddPlotImages(request):
    context = {}
    if request.method =='POST':
        properties = request.POST.get('properties')
        images = request.FILES.getlist('images')
        print(images,properties)
        for img in images:
            PropertiesImage.objects.create(properties_id = properties, image=img)
        messages.success(request, "Image Insert Successfully!")
        return redirect('/app/plot-image-list')
    plots = Properties.objects.all()
    context['plots'] = plots
    return render(request, 'app/add-plot-images.html', context)

@login_required(login_url='/accounts/auth-login/')
def PlotImagesList(request):
    context = {}
    images = PropertiesImage.objects.all()
    context['images'] = images
    return render(request, 'app/plot-image-list.html', context)

def DeletePlotImage(request, pk):
    obj = get_object_or_404(PropertiesImage, id=pk)
    obj.delete()
    messages.success(request, "Image delete successfully")
    return redirect('/app/plot-image-list')

def UpdatePlotImage(request, pk):
    obj = get_object_or_404(PropertiesImage, id=pk)
    
    if request.method == 'POST':
        form = PlotImageForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image updated successfully.')
            return redirect('/app/plot-image-list') 
    else:
        form = PlotImageForm(instance=obj)

    context = {'form': form}
    return render(request, 'app/edit-plot-image.html', context)

@login_required(login_url='/accounts/auth-login/')
def AddPlotAvailability(request):
    context = {}
    if request.method =='POST':
        try:
            form = AddPlotAvailabilityForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Plot Availability Added Successfully!')
                return redirect('/app/add-plot-availability')
            else:
                print(form.errors)
                form.errors['__all__'] = "Somethong wrong"
                return render(request, 'app/add-plot-availability.html', {'form':form})
        except Exception as e:
            print(e)
    form = AddPlotAvailabilityForm()
    context['form'] = form
    return render(request, 'app/add-plot-availability.html', context)

@login_required(login_url='/accounts/auth-login/')
def AddGalleryImage(request):
    context= {}
    if request.method =='POST':
        try:
            form = AddGalleryImagesForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully Inserted!')
                return redirect('/app/list-gallery-images')
            else:
                form.errors['__all__'] = "Somethong wrong"
                return render(request, 'app/add-gallery-image.html', {'form':form})
        except Exception as e:
            print(e)
    form = AddGalleryImagesForm
    context['form'] = form
    return render(request, 'app/add-gallery-image.html', context)
    
@login_required(login_url='/accounts/auth-login/')
def ListGalleryImages(request):
    context = {}
    try:
        gallery = GalleryImages.objects.all()
        context['gallery'] = gallery
    except Exception as e:
        print(e)
    return render(request, 'app/list-gallery-images.html', context)

@login_required(login_url='/accounts/auth-login/')
def DeleteImageView(request, pk):
    obj = get_object_or_404(GalleryImages, pk=pk)
    obj.delete()
    messages.success(request, "Image deleted successfully.")
    return redirect('/app/list-gallery-images')


@login_required(login_url='/accounts/auth-login/')
def MyOrdersView(request):
    contaxt = {}
    try:
        my_orders = PlotBooking.objects.filter(associate_id=request.user.sponsor_id).order_by('-created_at')
        contaxt['my_orders']= my_orders
    except Exception as e:
        print(e)
    return render(request, 'app/my-orders.html', contaxt)


from django.http import JsonResponse


def getAgentBookedDetailsView(request):
    booking_id = request.GET.get('booking_id')
    try:
        booking_details = PlotBooking.objects.get(id=booking_id)
        print(booking_details.agent)
        serialized_data = {
            'id': booking_details.id,
            'agent': booking_details.agent.email,
            'payment_method': booking_details.payment_method,
            'total_amount': booking_details.total_amount,
            'emi_period': booking_details.emi_period,
            'down_payment': booking_details.down_payment,
            # ... add other fields you want to include
        }
        return JsonResponse(serialized_data)
    except PlotBooking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404)
    
@login_required(login_url='/accounts/auth-login/')
def AddRewardView(request):
    context = {}
    if request.method == 'POST':
        try:
            form = RewardForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Reward Added Successfully!")
                return redirect('/app/reward-list')
            else:
                form.errors['__all__'] = "Somethong wrong"
                print(form.errors)
                return render(request, 'app/add-reward.html', {'form':form})
        except Exception as e:
            print(e)
    form = RewardForm()
    context['form'] = form
    return render(request, "app/add-reward.html", context)

@login_required(login_url='/accounts/auth-login/')
def RewardListView(request):
    context = {}
    try:
        rewards = Reward.objects.all()
        context['rewards'] = rewards
    except Exception as e:
        print(e)
    return render(request, "app/reward-list.html", context)

@login_required(login_url='/accounts/auth-login/')
def UpdateRewardView(request, pk):
    reward_instance = get_object_or_404(Reward, pk=pk)
    if request.method == 'POST':
        form = RewardForm(request.POST, instance=reward_instance)
        if form.is_valid(): 
            form.save()
            messages.success(request, "Reward Updated Successfully")
            return redirect('/app/reward-list') 
    else:
        form = RewardForm(instance=reward_instance)
    context = {'form': form}
    return render(request, "app/update-reward.html", context)

@login_required(login_url='/accounts/auth-login/')
def DeleteRewardView(request, pk):
    reward_instance = get_object_or_404(Reward, pk=pk)
    reward_instance.delete()
    messages.success(request, "Reward Deleted Successfully")
    return redirect('/app/reward-list')
    

@login_required(login_url='/accounts/auth-login/')
def FacilitatorListView(request):
    context = {}
    try:
        facilitators = CustomUser.objects.all().exclude(is_superuser=True).order_by('date_joined')
        context['facilitators'] = facilitators
    except Exception as e:
        print(e)
    return render(request, "app/facilitator-list.html", context)


@login_required(login_url='/accounts/auth-login/')
def TransferRequestView(request):
    context = {}
    if request.method =='POST':
        try:
            form = TransferRequestForm(request.POST)
            if form.is_valid():
                walletObject = Wallet.objects.get(associate=request.user)
                amount = form.cleaned_data.get('amount')
                
                if amount > walletObject.wallet_balance:
                    print("this is error")
                    form.add_error('amount', "Insufficient balance")
                    return render(request, "app/fund-transfer-request.html", {'form' : form})
                transfer_request = form.save(commit=False)
                transfer_request.user = request.user
                transfer_request.status = "pending"
                walletObject.wallet_balance -=amount
                walletObject.save()
                transfer_request.save()
                messages.success(request, "Your transfer request has been successfully sent")
                return redirect('/app/transfer-request')
        except Exception as e:
            print(e)
    balance = Wallet.objects.filter(associate_id = request.user.account_id).aggregate(wallet_balance = Sum("wallet_balance"))
    form = TransferRequestForm()
    context['form'] = form
    context['balance'] = balance
    return render(request, "app/fund-transfer-request.html", context)

@login_required(login_url='/accounts/auth-login/')
def TransferRequestListView(request):
    context = {}
    try:
        transfers = TransferRequest.objects.filter(user=request.user)
        context['transfers'] = transfers
    except Exception as e:
        print(e)
    return render(request, "app/fund-transfer-request-list.html", context)

@login_required(login_url='/accounts/auth-login/')
def WithdrawalsRequestListView(request):
    context = {}
    try:
        withdrawals = TransferRequest.objects.all().order_by('-created_at')
        context['withdrawals'] = withdrawals
    except Exception as e:
        print(e)
    return render(request, "app/withdrawals-request.html", context)

@login_required(login_url='/accounts/auth-login/')
def ViewAgentWithrawalsDetailsView(request, transfer_request_id):
    if not request.user.is_accountent and request.user.is_admin and request.user.is_staff:
        messages.warning(request, "You have not permission to access this page")
        return redirect('/app/')
    transfer_request = get_object_or_404(TransferRequest, pk=transfer_request_id)
    bank_details = CustomUser.objects.filter(email=transfer_request.user).first()
    print(bank_details)
    if request.method == 'POST':
        form = WithdrawalsRequestForm(request.POST, instance=transfer_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Status updated successfully!")
            return redirect('/app/withdrawals-list')  # Redirect to the appropriate page
    else:
        form = WithdrawalsRequestForm(instance=transfer_request)
    
    return render(request, 'app/view-withdrawals-details.html', {'form': form, 'bank_details':bank_details})

@login_required(login_url='/accounts/auth-login/')
def BookingHistoryView(request):
    context = {}
    try:
        booking_history = PlotBooking.objects.all()
        context['booking_history'] = booking_history
    except Exception as e:
        print(e)
    return render(request, "app/booking-history.html", context)

@login_required(login_url='/accounts/auth-login/')
def PlotBookingView(request):
    context = {}
    if request.method == 'POST':
        try:
            form = PlotBookingForm(request.POST)
            if form.is_valid():
                booking_id = generate_booking_id()
                form_obj = form.save(commit=False)
                form_obj.booking_id = booking_id
                customerName = form.cleaned_data.get('customer_name')
                email = form.cleaned_data.get('customer_email')
                associate_id = form.cleaned_data.get('associate_id')
                total_amount = form.cleaned_data.get('total_amount')
                pay_payment = form.cleaned_data.get('down_payment')
                emi_period = form.cleaned_data.get('emi_period')
                booking_method = form.cleaned_data.get('booking_method')
                customer_username = email.split('@')[0]
                customer_password = CustomUser.objects.make_random_password()
                if pay_payment is None:
                    pay_payment = total_amount
                form_obj.customer_username = customer_username
                form_obj.customer_password = customer_password
                form_obj.save()
                amount = form_obj.remaining_balance
                if booking_method == 'EMI':
                    convert_into_emi(amount, booking_id, emi_period)
                associate = CustomUser.objects.filter(sponsor_id=associate_id).first()
                if associate is None:
                    form.add_error('associate_id', "Invalid associate id")
                    context['form'] = form
                    return render(request, "app/plots-booking.html", context)
                commission = calculate_commission(pay_payment, associate.business_level)
                agent_wallet, created = Wallet.objects.get_or_create(associate_id=associate.account_id)
                agent_wallet.wallet_balance += commission
                agent_wallet.total_business += pay_payment
                agent_wallet.is_active = True
                agent_wallet.save()
                commission_level = find_commission_level(agent_wallet.total_business)
                if commission_level:
                    print(f"Commission Level for {agent_wallet.total_business}: {commission_level}")
                    associate.business_level = commission_level
                    associate.is_wallet_active = True
                    associate.save()
                else:
                    print("Total amount exceeds the highest slab.")
                html_content = f"Dear {customerName},Your booking has been successfully confirmed. Your login ID Username: {customer_username} and Password: {customer_password} Thank you for choosing Recon Group."
                html_content2 = f"Dear {associate.first_name},Your booking has been successfully confirmed booking id {booking_id}.Thank you for choosing Recon Group."
                subject ="Booking Confirmation"
                send_email(html_content, subject, email)
                send_email2(html_content2, subject, associate.email)
                messages.success(request, "Payment Saved Successfully!")
                return redirect('/app/booking-history')
            context['form'] = form
            return render(request, "app/plots-booking.html", context)
        except Exception as e:
            print("An error occurred:",e)
    form = PlotBookingForm()
    context['form'] = form
    return render(request, "app/plots-booking.html", context)


@login_required(login_url='/accounts/auth-login/')
def UpdateBookingPlot(request, booking_id):
    obj = get_object_or_404(PlotBooking, pk = booking_id)
    if request.method =='POST':
        form = PlotBookingForm(request.POST, instance=obj)
        if form.is_valid():
            form_obj = form.save()
            customerName = form.cleaned_data.get('customer_name')
            email = form.cleaned_data.get('customer_email')
            associate_id = form.cleaned_data.get('associate_id')
            total_amount = form.cleaned_data.get('total_amount')
            pay_payment = form.cleaned_data.get('down_payment')
            booking_status = form.cleaned_data.get('booking_status')

            if pay_payment is None:
                    pay_payment = total_amount
            # print(pay_payment,"877777777777777777777777777777")
            # if pay_payment:
            #     remaining_balance = total_amount - pay_payment
            #     print(remaining_balance,"877777777777")
            #     form_obj.remaining_balance = remaining_balance
            #     form_obj.customer_username = customer_username
            #     form_obj.save()
            # else:
            #     print("45555555555555555555555555555555554")
            #     form_obj.customer_username = customer_username
            #     pay_payment = total_amount
            #     form_obj.save()
            associate = CustomUser.objects.filter(sponsor_id=associate_id).first()
            if associate is None:
                form.add_error('associate_id', "Invalid associate id")
                context['form'] = form
                return render(request, "app/plots-booking.html", context)
            commission = calculate_commission(pay_payment, associate.business_level)
            agent_wallet, created = Wallet.objects.get_or_create(associate_id=associate.account_id)
            agent_wallet.wallet_balance += commission
            agent_wallet.total_business += pay_payment
            agent_wallet.is_active = True
            agent_wallet.save()
            commission_level = find_commission_level(agent_wallet.total_business)
            if commission_level:
                print(f"Commission Level for {agent_wallet.total_business}: {commission_level}")
                associate.business_level = commission_level
                associate.save()
            else:
                print("Total amount exceeds the highest slab.")
            html_content = f"Dear {customerName}! We are delighted to inform you that your booking with Recon Group has been {booking_status}."
            subject ="Booking Confirmation"
            send_email(html_content, subject, email)
            messages.success(request, "Booking updated successfully!")
            return redirect('/app/booking-history')
    else:
        form = PlotBookingForm(instance= obj)
    return render(request, "app/edit-booking-plot.html", {'form' : form})

@login_required(login_url='/accounts/auth-login/')
def DeleteBookingView(request, booking_id):
    try:
        obj = get_object_or_404(PlotBooking, pk = booking_id)
        obj.delete()
        messages.success(request, "Plot Booking History Deleted Successfully!")
        return redirect('/app/booking-history')
    except Exception as e:
        print(e)

from django.http import JsonResponse
def ActivateIdView(request):
    if request.method =='POST':
        sponsor_id = request.POST.get('id')
        print(sponsor_id)
        user = CustomUser.objects.get(sponsor_id=sponsor_id)
        if user.is_wallet_active is True:
            user.is_wallet_active = False
        else:
            user.is_wallet_active = True
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error_message': 'Item not found'})


@login_required(login_url='/accounts/auth-login/')
def MyTreeTeamView(request):
    return render(request, 'app/tree-team.html')


from django.http import JsonResponse
def GetAllUsersView(request):
    def build_team_tree(user):
        children = CustomUser.objects.filter(referred_by_id=user.account_id)
        children_list = []
        for child in children:
            amount = PlotBooking.objects.filter(associate_id=child.sponsor_id).aggregate(wallet_balance = Sum("down_payment"))['wallet_balance'],
            
            converted_amount = amount_human_format(amount[0])
            child_data = {
                "name": child.first_name+ ' ' + child.last_name,
                "sponsor_id": child.sponsor_id,
                "business_level": child.business_level,
                "total_business": amount[0] or 0,
                "image": '/static/app-assets/media/user-icon.png',
                "children": build_team_tree(child) 
            }
            children_list.append(child_data)
        return children_list

    superusers = CustomUser.objects.filter(account_id=request.user.account_id)
    teams_list = []
    for superuser in superusers:
        converted_amount = 0
        if request.user.is_superuser:
            amount = PlotBooking.objects.all().aggregate(wallet_balance = Sum("down_payment"))['wallet_balance'],
            converted_amount = amount[0] or 0
        else:
            amount = PlotBooking.objects.filter(associate_id=request.user.sponsor_id).aggregate(wallet_balance = Sum("down_payment"))['wallet_balance'],
        converted_amount = amount[0] or 0
        team_data = {
            "name": superuser.first_name+ ' ' + superuser.last_name,
            "sponsor_id": superuser.sponsor_id,
            "business_level": superuser.business_level,
            "total_business": converted_amount,
            "image": '/static/app-assets/media/logos/page-loader.png',
            "children": build_team_tree(superuser)  
        }
        teams_list.append(team_data)

    print(teams_list, "87777777777777777")
    return JsonResponse(teams_list, safe=False)



def EMIHistoryView(request):
    context = {}
    booking_id = request.GET.get('booking_id')
    print(booking_id)
    if request.method =='POST':
        search_query = request.POST.get('query')
        bookings = PlotBooking.objects.filter(booking_id=search_query).first()
        if bookings is None:
            messages.error(request, "No Data Found! Please enter valid Booking ID")
            return redirect('/app/emi-history')
        result = EMIHistory.objects.filter(booking_id = search_query)
        list_data = []
        for x in result:
            data  = {
                "associate_id": bookings.associate_id,
                "customer_name": bookings.customer_name,
                "customer_phone": bookings.customer_phone,
                "emi_due_date": x.emi_date,
                "amount": x.emi_amount,
                "emi_status": x.is_paid,
                "booking_id": x.booking_id,
                "emi_id": x.id,
            }
            list_data.append(data)
        context['result'] = list_data
        context['booking'] = bookings
        context['search_query'] = search_query
        return render(request, "app/emi-history.html", context)
    if booking_id:
        bookings = PlotBooking.objects.filter(booking_id=booking_id).first()
        if bookings is None:
            messages.error(request, "No Data Found! Please enter valid Booking ID")
            return redirect('/app/emi-history')
        result = EMIHistory.objects.filter(booking_id = booking_id)
        list_data = []
        for x in result:
            data  = {
                "associate_id": bookings.associate_id,
                "customer_name": bookings.customer_name,
                "customer_phone": bookings.customer_phone,
                "emi_due_date": x.emi_date,
                "amount": x.emi_amount,
                "emi_status": x.is_paid,
                "booking_id": booking_id,
                "emi_id": x.id,
                
            }
            list_data.append(data)
        context['result'] = list_data
        context['booking'] = bookings
    return render(request, "app/emi-history.html", context)


def PayEMIView(request):
    if request.method == 'POST':
        emi_id = request.POST.get('emi_id')
        booking_id = request.POST.get('booking_id')
        status = request.POST.get('status')
        print(booking_id,"7878787")
        try:
            booking = EMIHistory.objects.get(id=emi_id)
            booking.is_paid = status
            booking.save()
            booking_details = PlotBooking.objects.filter(booking_id=booking_id).first()
            print(booking_details)
            wallet_object = Wallet.objects.get(associate__sponsor_id = booking_details.associate_id)
            commission = calculate_commission(booking.emi_amount, wallet_object.business_level)
            wallet_object.wallet_balance +=commission
            booking_details.remaining_balance -=booking.emi_amount
            booking_details.down_payment +=booking.emi_amount
            booking_details.save()
            wallet_object.save()
            html_content = f"Hi {booking_details.customer_name} Your EMI payment has been successfully processed."
            subject = "EMI Payment Confirmation"
            email = booking_details.customer_email
            # send_email(html_content, subject, email)
            return JsonResponse({'success': True})
        except EMIHistory.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Booking not found'})
    return JsonResponse({'success': False, 'error_message': 'Invalid request'})





def MyWalletView(request):
    context = {}
    wallet_balance = Wallet.objects.filter(associate = request.user).aggregate(wallet=Sum('wallet_balance'))['wallet']
    withdrawals = TransferRequest.objects.filter(user=request.user).aggregate(withdrawal=Sum('amount'))['withdrawal']
    context['wallet_balance'] = wallet_balance
    context['withdrawals'] = withdrawals
    return render(request, 'app/wallet.html', context)