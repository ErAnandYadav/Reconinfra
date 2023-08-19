from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Sum
from django.conf import settings
from Reconinfra_Accounts.models import *
from .helpers import *
from .forms import *
from .models import *
import random
# Create your views here.
@login_required(login_url='/accounts/auth-login/')
def Admin_Panel_Home(request):
    context = {}
    try:
        balance = Wallet.objects.filter(agent_id = request.user.account_id).aggregate(wallet_balance = Sum("balance"))
        context['balance'] = balance
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
        images = request.POST.getlist('images')
        print(images,properties)
        for img in images:
            PropertiesImage.objects.create(properties_id = properties, image=img)
            messages.success(request, "Image Insert Successfully!")
            return redirect('/app/add-plot-images')
    plots = Properties.objects.all()
    context['plots'] = plots
    return render(request, 'app/add-plot-images.html', context)


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
                return redirect('/app/add-gallery-images')
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


# @login_required(login_url='/accounts/auth-login/')
# def PlotBookingView(request):
#     context = {}
#     if request.method =='POST':
#         try:
#             form = PlotBookingForm(request.POST, request.FILES)
#             if form.is_valid():
#                 total_amount = form.cleaned_data.get('total_amount')
#                 down_payment = form.cleaned_data.get('down_payment')
#                 # calculate min 20 %
#                 perc = total_amount * 20 / 100
#                 if down_payment != perc:
#                     form.add_error('down_payment', "Booking Amount Minimum 20%")
#                     return render(request, 'app/plot-booking.html', {'form' : form})
#                 booking_obj =form.save()
#                 pin = pin_generate()
#                 booking_obj.pin = pin
#                 booking_obj.agent_id = request.user.account_id
#                 booking_obj.save()
#                 subject = 'Welcome to Recon Group'
#                 message = f'Congratulation {request.user.first_name}, Your Plot Booking PIN(Payment Identification Number) is {pin}'
#                 email_from = settings.EMAIL_HOST_USER
#                 recipient_list = [request.user.email, ]
#                 try:
#                     send_mail( subject, message, email_from, recipient_list )
#                 except Exception as e:
#                     print(e)

#                 # Bronze - Less than 1500 points.
#                 # Silver - 1500-1999 points.
#                 # Gold - 2000-2499 points.
#                 # Platinum - 2500-2999 points.
#                 # Diamond - 3000-3499 points.
#                 # Master - More than 3500 points.
#                 # Grandmaster - Top 500 players in the ranked leaderboard.

#                 wallet_balance = Wallet.objects.filter(agent_id = request.user.account_id).aggregate(total_balance = Sum('balance'))
#                 print("wallet_balance",wallet_balance)

#                 if wallet_balance['total_balance'] is None:
#                     _5_perc_com = down_payment * 5 / 100 
#                     Wallet.objects.create(agent_id = request.user.account_id,balance=_5_perc_com)

#                 # amount = [0, 2500000, 5000000, 10000000, 50000000, 100000000]
#                 # for amt in amount:
#                 #     print("ammount Loop", amt)

#                 if wallet_balance['total_balance'] <= 2500000: # 0 to 25lac
#                     print("5% Commission Slab")
#                     _5_perc = down_payment * 5 / 100 
#                     Wallet.objects.create(agent_id = request.user.account_id, balance=_5_perc)

#                 elif wallet_balance['total_balance'] <= 5000000: # 25lac to 50lac
#                     print("8% Commission Slab")
#                     _8_perc = down_payment * 8 / 100
#                     Wallet.objects.create(agent_id = request.user.account_id, balance=_8_perc)
                    
#                 elif wallet <= 10000000: # 50lac to 1cr
#                     print("10% Commission Slab")
#                     _10_perc = down_payment * 10 / 100
#                     Wallet.objects.create(agent_id = request.user.account_id, balance=_10_perc)
                    
#                 elif wallet <= 50000000: # 1cr to 5cr
#                     print("12% Commission Slab")
#                     _12_perc = down_payment * 12 / 100
#                     Wallet.objects.create(agent_id = request.user.account_id, balance=_12_perc)

#                 elif wallet <= 100000000: # 5cr to 10cr
#                     print("14% Commission Slab")
#                     _14_perc = down_payment * 14 / 100
#                     Wallet.objects.create(agent_id = request.user.account_id, balance=_14_perc)

#                 elif wallet > 100000000: # 10cr to Above
#                     print("15% Commission Slab")
#                     _15_perc = down_payment * 15 / 100
#                     Wallet.objects.create(agent_id = request.user.account_id, balance=_15_perc)

#                 messages.success(request, "Plot Booked Successfully")
#                 return redirect('/app/booking-list')
#             else:
#                 form.errors['__all__'] = "Somethong wrong"
#                 print(form.errors)
#                 return render(request, 'app/plot-booking.html', {'form':form})
#         except Exception as e:
#             print(e)
#     form = PlotBookingForm()
#     context['form'] = form
#     return render(request, 'app/plot-booking.html', context)


@login_required(login_url='/accounts/auth-login/')
def PlotBookingView(request):
    context = {}
    if request.method =='POST':
        try:
            form = PlotBookingForm(request.POST)
            if form.is_valid():
                form_obj = form.save(commit=False)
                form_obj.agent_id = request.user.account_id
                booking_id = generate_booking_id()
                form_obj.booking_id = booking_id
                pin = pin_generate() # Generate 4 Digit PIN
                form_obj.pin = pin
                form_obj.save()
                subject = 'Welcome to the Recon Group'
                message = f'Congratulation {request.user.first_name}, Your Booking ID is {booking_id} and Your PIN (Personal identification numbers) is {pin} Please do not share your booking ID Thank You!'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email, ]
                try:
                    send_mail( subject, message, email_from, recipient_list )
                except Exception as e:
                    print(e)
                messages.success(request, "Your Plot Booked Successfully")
                return redirect('/app/booking-list')
            else:
                form.errors['__all__'] = "Somethong wrong"
                print(form.errors)
                return render(request, 'app/plot-booking.html', {'form':form})
        except Exception as e:
            print("Error", e)
    form = PlotBookingForm()
    context['form'] = form
    return render(request, 'app/plot-booking.html', context)

@login_required(login_url='/accounts/auth-login/')
def BookingList(request):
    contaxt = {}
    try:
        booking_plot = PlotBooking.objects.filter(agent=request.user).order_by('-created_at')
        contaxt['booking_plot']= booking_plot
    except Exception as e:
        print(e)
    return render(request, 'app/booking-list.html', contaxt)

@login_required(login_url='/accounts/auth-login/')
def UpdateBookingPlot(request, booking_id):
    obj = get_object_or_404(PlotBooking, pk = booking_id)
    if request.method =='POST':
        form = PlotBookingForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully!")
            return redirect('/app/booking-list')
    else:
        form = PlotBookingForm(instance= obj)
    return render(request, "app/edit-booking-plot.html", {'form' : form})

from django.http import JsonResponse


def getAgentBookedDetailsView(request):
    booking_id = request.GET.get('booking_id')
    try:
        booking_details = PlotBooking.objects.get(id=booking_id)
        serialized_data = {
            'id': booking_details.id,
            'agent': booking_details.agent,  # Replace with your actual fields
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
def AddPaymentView(request):
    context = {}
    if request.method=='POST':
        form = PaymentHistoryForm(request.POST)
        if form.is_valid():
            form_obj =form.save(commit=False)
            agent = form.cleaned_data.get('agent')
            pay_payment = form.cleaned_data.get('pay_payment')
            booking = form.cleaned_data.get('booking')
            total_amount = form.cleaned_data.get('total_amount')
            remaining_balance = total_amount - pay_payment
            form_obj.remaining_balance = remaining_balance
            form_obj.save()
            
            total_business = PaymentHistory.objects.filter(agent=agent).aggregate(amount = Sum('pay_payment'))
            print(total_business['amount'])
            # Commissions Create
            if total_business['amount'] <= 2500000: # 0 To 25lac
                print("5% Commission Slab")
                _5_perc_com = total_business['amount'] * 5 / 100
                agent_wallet = Wallet.objects.filter(agent_id = agent.account_id)
                if not agent_wallet:
                    Wallet.objects.create(agent_id = agent.account_id, balance = _5_perc_com)
                else:
                    wallet_obj = Wallet.objects.get(agent_id = agent.account_id)
                    wallet_obj.balance += _5_perc_com
                    wallet_obj.save()
            
            elif total_business['amount'] <= 5000000: # 25lac To 50lac
                print("8% Commission")
                _8_perc_com = total_business['amount'] * 8 / 100 
                agent_wallet = Wallet.objects.get(agent_id = agent.account_id)
                agent_wallet.balance += _8_perc_com
                agent_wallet.save()

            elif total_business['amount'] <= 10000000: # 50lac to 1cr
                print("10% Commission")
                _10_perc_com = total_business['amount'] * 10 / 100
                agent_wallet = Wallet.objects.get(agent_id = agent.account_id)
                agent_wallet.balance += _10_perc_com
                agent_wallet.save()

            elif total_business['amount'] <= 50000000: # 1cr To 5cr
                print("12% Commission")
                _12_perc_com = total_business['amount'] * 12 / 100
                agent_wallet = Wallet.objects.get(agent_id = agent.account_id)
                agent_wallet.balance += _12_perc_com
                agent_wallet.save()

            elif total_business['amount'] <= 100000000: # 5cr  To 10cr
                print("14% Commission")
                _14_perc_com = total_business['amount'] * 14 / 100
                agent_wallet = Wallet.objects.get(agent_id = agent.account_id)
                agent_wallet.balance += _14_perc_com
                agent_wallet.save()

            elif total_business['amount'] < 100000000: # 10cr To Above
                print("15% Commission")
                _15_perc_com = total_business['amount'] * 15 / 100
                agent_wallet = Wallet.objects.get(agent_id = agent.account_id)
                agent_wallet.balance += _15_perc_com
                agent_wallet.save()

            messages.success(request, "Payment Save Successfully!")
            return redirect('/app/payment-history')
    form = PaymentHistoryForm()
    context['form'] = form
    return render(request, 'app/add-payment.html', context)

@login_required(login_url='/accounts/auth-login/')
def PaymentHistoryView(request):
    context = {}
    try:
        payment_history = PaymentHistory.objects.all()
        context['payment_history'] = payment_history
    except Exception as e:
        print(e)
    return render(request, "app/payment-history.html", context)

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
        rewards = Reward.objects.all().order_by('-date_time')
        context['rewards'] = rewards
    except Exception as e:
        print(e)
    return render(request, "app/reward-list.html", context)

@login_required(login_url='/accounts/auth-login/')
def FacilitatorListView(request):
    context = {}
    try:
        facilitators = CustomUser.objects.all()
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
                walletObject = Wallet.objects.get(agent=request.user)
                amount = form.cleaned_data.get('amount')
                if amount > walletObject.balance:
                    print("this is error")
                    form.add_error('amount', "Insufficient balance")
                    return render(request, "app/fund-transfer-request.html", {'form' : form})
                transfer_request = form.save(commit=False)
                transfer_request.user = request.user
                transfer_request.status = "pending"
                walletObject.balance -=amount
                walletObject.save()
                transfer_request.save()
                messages.success(request, "Your transfer request has been successfully sent")
                return redirect('/app/transfer-request')
        except Exception as e:
            print(e)
    balance = Wallet.objects.filter(agent_id = request.user.account_id).aggregate(wallet_balance = Sum("balance"))
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