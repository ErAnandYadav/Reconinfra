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
            
            balance = PlotBooking.objects.all().exclude(booking_status ="Saved").aggregate(total_business = Sum("down_payment"))
            monthly_business = PlotBooking.objects.filter(query).exclude(booking_status ="Saved").aggregate(monthly_business=Sum('down_payment'))['monthly_business']
            context['balance'] = balance
            context['monthly_business'] = monthly_business
            activeUser = CustomUser.objects.filter(is_wallet_active = True).exclude(is_superuser=True).count
            inactiveUser = CustomUser.objects.filter(is_wallet_active = False).exclude(is_superuser=True).count
            context['activeUser'] = activeUser
            context['inactiveUser'] = inactiveUser
            rewards = Reward.objects.all()
        else:
            balance = PlotBooking.objects.filter(associate_id= request.user.sponsor_id).exclude(booking_status ="Saved").aggregate(total_business = Sum("down_payment")) or 0
            
            print(balance)
            monthly_business = PlotBooking.objects.filter(query).filter(associate_id=request.user.sponsor_id).exclude(booking_status ="Saved").aggregate(monthly_business=Sum('down_payment'))['monthly_business'] or 0.00
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
    print("Function work")
    context = {}
    if request.method =='POST':
        print("post working")
        form = AddPlotAvailabilityForm(request.POST)
        
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plot Availability Added Successfully!')
            return redirect('/app/add-plot-availability')
        print(form.add_error)
        form.errors['__all__'] = "Somethong wrong"
        return render(request, 'app/add-plot-availability.html', {'form':form})
       
    form = AddPlotAvailabilityForm()
    context['form'] = form
    return render(request, 'app/add-plot-availability.html', context)

def ChoosePlot(request):
    context = {}
    plots = Properties.objects.all()
    context['plots'] = plots
    return render(request, 'app/choose-plot.html', context)

def UpdatePlotAvailability(request, plot_id):
    if request.method =='POST':
        plot_number = request.POST.get('plot_number')
        print(plot_number,"][][][]][]")
        status = request.POST.get('status')
        instance = PlotAvailabilities.objects.get(plot_number = plot_number)
        instance.plot_status = status
        instance.save()
        messages.success(request, f"Plot number {plot_number} is {status} successfully!")
        return redirect('/app/choose-plot')
    context = {}
    instance = PlotAvailabilities.objects.filter(properties_id = plot_id)
    context['plot_number'] = instance
    return render(request, 'app/update-plot-availability.html', context)

def GetPlotNumber(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id)
    city_list = [{"id": city.id, "name": city.name} for city in cities]
    return JsonResponse({"cities": city_list})

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

from django.db.models import Sum, F
@login_required(login_url='/accounts/auth-login/')

def AssociateRewardListView(request):
    context = {}
    try:
        user_sponsor_id = request.user.sponsor_id
        balance = PlotBooking.objects.filter(associate_id=user_sponsor_id).exclude(booking_status="Saved").aggregate(total_business=Sum(F("down_payment")))['total_business'] or 0
        print(balance)

        rewards = Reward.objects.all()
        rewards_list = []
        for i in range(len(rewards) - 1):
            rm_balance = rewards[i + 1].business - rewards[i].business
            progress = min(round((balance / rm_balance) * 100, 2), 100)
            print(f"Subtracting {rewards[i].business} from {rewards[i + 1].business}: Result = {rm_balance}")
            if progress == 100 and rewards[i].status == 'Lock':
                rewards[i].status = 'Unlock'
                rewards[i].save()

            data = {
                "id": rewards[i].id,
                "title": rewards[i].title,
                "product_type": rewards[i].product_type,
                "description": rewards[i].description,
                "business": rewards[i].business,
                "product_image": rewards[i].product_image,
                "is_lock": rewards[i].is_lock,
                "status": rewards[i].status,
                "time_limit": rewards[i].time_limit,
                "progress": progress,
            }
            rewards_list.append(data)

        context['rewards'] = rewards_list

    except Exception as e:
        print(e)

    return render(request, "app/associate-reward-list.html", context)


def ClaimRewardView(request):
    reward_id = request.GET.get('reward_id')
    associate = request.user
    print(reward_id)
    reward = Reward.objects.get(id = reward_id)
    print(reward)
    ClaimedReward.objects.create(reward=reward, associate=associate, status="Requested")
    reward.is_lock = True
    reward.status = 'Claimed'
    reward.save()
    return JsonResponse({'status':200})

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
def PayoutTransferView(request):
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
        booking_history = PlotBooking.objects.all().exclude(booking_status = 'Saved')
        context['booking_history'] = booking_history
    except Exception as e:
        print(e)
    return render(request, "app/booking-history.html", context)

@login_required(login_url='/accounts/auth-login/')
def SavedBookingFormView(request):
    context = {}
    try:
        booking_history = PlotBooking.objects.filter(booking_status = 'Saved')
        context['booking_history'] = booking_history
    except Exception as e:
        print(e)
    return render(request, "app/saved-booking.html", context)

@login_required(login_url='/accounts/auth-login/')
def AddPaymentView(request, booking_id):
    context = {}
    try:
        if request.method =='POST':
            status = request.POST.get('status')
            booking_id = request.POST.get('booking_id')
            payment_method = request.POST.get('payment_method')
            number = request.POST.get('number')
            payment_date = request.POST.get('payment_date')
            form = AddPaymentForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data.get('amount')
                plots_booking = PlotBooking.objects.filter(booking_id=booking_id).first()
                form_obj = form.save()
                form_obj.is_paid = True
                form_obj.booking_status = status
                form_obj.save()
                plots_booking.remaining_balance -=amount
                plots_booking.down_payment +=amount
                plots_booking.booking_status = status
                plots_booking.save()
                if status == 'Approved':
                    update_commissions(booking_id)
                messages.success(request, "Payment added successfully")
                return redirect('/app/saved-booking-form')
            context['form'] = form
            context['booking_id'] = booking_id
            return render(request, "app/add-payment.html",  context)
        form = AddPaymentForm()
        context['form'] = form
        context['booking_id'] = booking_id
    except Exception as e:
        print(e)
    return render(request, "app/add-payment.html",  context)


def update_commissions(booking_id):
    try:
        paid_amount = EMIHistory.objects.filter(booking_id=booking_id).aggregate(paid_amount = Sum('amount'))['paid_amount']
        print("paid_amount:-", paid_amount)
        plot_booking = PlotBooking.objects.filter(booking_id=booking_id).first()
        booking_date = plot_booking.booking_date
        associate_id = plot_booking.associate_id
        total_amount = plot_booking.total_amount
        remaining_balance = total_amount - paid_amount
        print('remaining_balance', remaining_balance)
        emi_period = plot_booking.emi_period
        print("emi_period:", emi_period)
        associate = CustomUser.objects.filter(sponsor_id=associate_id).first()
        business_level = associate.business_level
        print('business_level:', business_level)
        if associate is None:
            form.add_error('associate_id', "Invalid associate id")
            context['form'] = form
            return render(request, "app/plots-booking.html", context)
    
        associate_total_business = PlotBooking.objects.filter(associate_id=associate.sponsor_id).exclude(booking_status ="Saved").aggregate(total_bisness = Sum('down_payment'))['total_bisness']
        commission_level = find_commission_level(associate_total_business)
        convert_into_emi(remaining_balance, booking_id, emi_period)
        commission_distribution(paid_amount, associate_id)
        if commission_level:
            print(f"Commission Level for {associate_total_business}: {commission_level}")
            associate.business_level = commission_level
            associate.is_wallet_active = True
            associate.save()
        else:
            print("Total amount exceeds the highest slab.")
        return True
    except Exception as e:
        print(e)
        return e

def if_full_payment(booking_id):
    try:
        plot_booking = PlotBooking.objects.filter(booking_id=booking_id).first()
        print(plot_booking,"8787545")
        associate_id = plot_booking.associate_id
        amount = plot_booking.down_payment
        associate = CustomUser.objects.filter(sponsor_id=associate_id).first()
        business_level = associate.business_level
        print('business_level:', business_level)
        if associate is None:
            form.add_error('associate_id', "Invalid associate id")
            context['form'] = form
            return render(request, "app/plots-booking.html", context)

        commission_distribution(amount, associate_id)
        
        associate_total_business = PlotBooking.objects.filter(associate_id=associate.sponsor_id).exclude(booking_status ="Saved").aggregate(total_bisness = Sum('down_payment'))['total_bisness']
        commission_level = find_commission_level(associate_total_business)
        if commission_level:
            print(f"Commission Level for {associate_total_business}: {commission_level}")
            associate.business_level = commission_level
            associate.is_wallet_active = True
            associate.save()
        else:
            print("Total amount exceeds the highest slab.")
        return True
    except Exception as e:
        print(e,"5454")
        return e

@login_required(login_url='/accounts/auth-login/')
def PlotBookingView(request):
    context = {}
    if request.method == 'POST':
        try:
            form = PlotBookingForm(request.POST)
            if form.is_valid():
                booking_id = generate_booking_id().upper()
                form_obj = form.save(commit=False)
                customerName = form.cleaned_data.get('customer_name')
                email = form.cleaned_data.get('customer_email')
                associate_id = form.cleaned_data.get('associate_id')
                total_amount = form.cleaned_data.get('total_amount')
                booking_amount = form.cleaned_data.get('down_payment')
                emi_period = form.cleaned_data.get('emi_period')
                booking_method = form.cleaned_data.get('booking_method')
                payment_method = form.cleaned_data.get('payment_method')
                booking_date = form.cleaned_data.get('booking_date')
                booking_status = form.cleaned_data.get('booking_status')
                cheque_number = form.cleaned_data.get('cheque_number')

                if booking_method == 'EMI' and booking_amount >= total_amount:
                    messages.error(request, "The booking amount must be less than the total amount.")
                    form.add_error("down_payment", "The booking amount must be less than the total amount.")
                    return render(request, "app/plots-booking.html", {'form':form})
                
                if booking_method =='Full Payment':
                    booking_amount = total_amount
                customer_username = email.split('@')[0]
                customer_password = CustomUser.objects.make_random_password()
                form_obj.customer_username = customer_username
                form_obj.customer_password = customer_password
                form_obj.booking_id = booking_id
                form_obj.down_payment = booking_amount
                form_obj.save()
                print(total_amount, booking_amount)
                
                if booking_method =='EMI' and booking_status =='Approved':
                    EMIHistory.objects.create(booking_id=booking_id, amount=booking_amount, payment_date=booking_date, booking_status=booking_status, payment_method=payment_method, number=cheque_number, is_paid=True)
                    update_commissions(booking_id)
                    
                         
                if booking_method =='Full Payment' and booking_status =='Approved':
                    print("Full Payment working",booking_amount)
                    if_full_payment(booking_id)
               
                html_content = f"Dear {customerName},Your booking has been successfully Saved. Your login ID Username: {customer_username}, Password: {customer_password} and your booking ID {booking_id}Thank you for choosing Recon Group."
                html_content2 = f"Dear random,Your booking has been successfully Saved booking id {booking_id}.Thank you for choosing Recon Group."
                subject ="Booking Confirmation"
                
                send_email(html_content, subject, email)
                send_email2(html_content2, subject, email)
                
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
def UpdateSavedForm(request, booking_id):
    plot_booking = get_object_or_404(PlotBooking, pk = booking_id)
    if request.method =='POST':
        form = PlotBookingForm(request.POST, instance=plot_booking)
        if form.is_valid():
            
            emi_period = form.cleaned_data.get('emi_period')
            associate_id = form.cleaned_data.get('associate_id')
            booking_method = form.cleaned_data.get('booking_method')
            booking_status = form.cleaned_data.get('booking_status')
            
            form_obj = form.save(commit=False)
            
            remaining_balance = form_obj.remaining_balance
            paid_amount = form_obj.down_payment
            booked_id = form_obj.booking_id
            
            associate_total_business = PlotBooking.objects.filter(associate_id=associate_id).exclude(booking_status ="Saved").aggregate(total_bisness = Sum('down_payment'))['total_bisness'] or 0
            commission_level = find_commission_level(associate_total_business)
            
            user = CustomUser.objects.get(sponsor_id=associate_id)
            
            if booking_method =='EMI' and booking_status =='Approved':
                convert_into_emi(remaining_balance, booked_id, emi_period)
                commission_distribution(paid_amount, associate_id)
                user.business_level = commission_level
                user.save()
                
            if booking_method =='Full Payment' and booking_status =='Approved':
                commission_distribution(paid_amount, associate_id)
                user.business_level = commission_level
                user.save()
                
            form_obj.save()
            messages.success(request, "Booking updated successfully!")
            return redirect('/app/saved-booking-form')
    else:
        form = PlotBookingForm(instance= plot_booking)
    return render(request, "app/update-saved-form-plot.html", {'form' : form})

@login_required(login_url='/accounts/auth-login/')
def ViewBookingHistory(request, booking_id):
    obj = get_object_or_404(PlotBooking, pk = booking_id)
    form = PlotBookingForm(instance= obj)
    return render(request, "app/view-booking-history.html", {'form' : form})


@login_required(login_url='/accounts/auth-login/')
def DeleteSavedFormView(request, booking_id):
    try:
        obj = get_object_or_404(PlotBooking, pk = booking_id)
        emi_instance = get_object_or_404(EMIHistory, booking_id = obj.booking_id)
        emi_instance.delete()
        obj.delete()
        messages.success(request, "Saved form and related data deleted successfully!")
        return redirect('/app/saved-booking-form')
    except Exception as e:
        print(e)
        messages.error(request, "Data not delete due to internal policy!")
        return redirect('/app/saved-booking-form')

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
def TreeTeamView(request):
    
    return render(request, 'app/team-tree-view.html')


def GetAllUsersView(request):
    def build_team_tree(user):
        children = CustomUser.objects.filter(referred_by_id=user.account_id)
        children_list = []
        for child in children:
            # amount = Wallet.objects.filter(associate=child).aggregate(wallet_balance = Sum("wallet_balance"))['wallet_balance'],
            amount = PlotBooking.objects.filter(associate_id=child.sponsor_id).exclude(booking_status ="Saved").aggregate(wallet_balance = Sum("down_payment"))['wallet_balance'],
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
            amount = PlotBooking.objects.all().exclude(booking_status ="Saved").aggregate(wallet_balance = Sum("down_payment"))['wallet_balance'],
            converted_amount = amount[0] or 0
        else:
            amount = PlotBooking.objects.filter(associate_id=request.user.sponsor_id).exclude(booking_status ="Saved").aggregate(wallet_balance = Sum("down_payment"))['wallet_balance'],
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

    
    return JsonResponse(teams_list, safe=False)


@login_required(login_url='/accounts/auth-login/')
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
                "emi_due_date": x.payment_date,
                "amount": x.amount,
                "payment_method": x.payment_method,
                "number": x.number or 'N/A',
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
            print(x.payment_method)
            data  = {
                "associate_id": bookings.associate_id,
                "customer_name": bookings.customer_name,
                "customer_phone": bookings.customer_phone,
                "emi_due_date": x.payment_date,
                "payment_method": x.payment_method,
                "number": x.number or 'N/A',
                "amount": x.amount,
                "emi_status": x.is_paid,
                "booking_id": booking_id,
                "emi_id": x.id,
            }
            list_data.append(data)
        context['result'] = list_data
        context['booking'] = bookings
    return render(request, "app/emi-history.html", context)


@login_required(login_url='/accounts/auth-login/')
def EMIPay(request, pk):
    emi_instance = get_object_or_404(EMIHistory, pk=pk)
    if request.method == 'POST':
        form = AddPaymentForm(request.POST, instance=emi_instance)
        if form.is_valid(): 
            booking_id = form.cleaned_data.get('booking_id')
            amount = form.cleaned_data.get('amount')
            print(amount)
            form.save()
            booking_details = PlotBooking.objects.filter(booking_id=booking_id).first()
            associate_id = booking_details.associate_id
            print(booking_details.remaining_balance -amount)
            commission_distribution(amount, associate_id)
            booking_details.remaining_balance -=amount
            booking_details.down_payment +=amount
            booking_details.save()
            messages.success(request, "EMI Paid Successfully")
            return redirect('/app/booking-history') 
        print(form.errors)
    else:
        form = AddPaymentForm(instance=emi_instance)
    context = {'form': form}
    return render(request, "app/pay-emi.html", context)
    

@login_required(login_url='/accounts/auth-login/')
def MyWalletView(request):
    context = {}
    wallet_balance = Wallet.objects.filter(associate = request.user).aggregate(wallet=Sum('wallet_balance'))['wallet']
    withdrawals = TransferRequest.objects.filter(user=request.user).aggregate(withdrawal=Sum('amount'))['withdrawal']
    context['wallet_balance'] = wallet_balance
    context['withdrawals'] = withdrawals
    return render(request, 'app/wallet.html', context)

@login_required(login_url='/accounts/auth-login/')
def TeamsSizeView(request):
    context = {}
    team_size = get_multilevel_chain_count(request.user)
    team_business = get_team_business(request.user)
    self_business = PlotBooking.objects.filter(associate_id=request.user.sponsor_id).exclude(booking_status ="Saved").aggregate(self_business=Sum('down_payment'))['self_business']
    context['team_size'] = team_size
    context['team_business'] = team_business
    context['self_business'] = self_business or 0.00
    return render(request, 'app/team-size.html', context)

def TestAllInOneAPI(request):
    user = request.user
    # Start counting from the request.user
    teams_size = get_multilevel_chain_count(user)
    total_team_business = get_team_business(user)
    level_up_with_teams_and_self_business(user)
    return JsonResponse({"status": 200, "multilevel_chain_count": teams_size, "total_team_business":total_team_business})

