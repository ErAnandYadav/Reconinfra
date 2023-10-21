from queue import PriorityQueue
from django.contrib import messages
from django.shortcuts import render, HttpResponse,redirect
from .forms import *
from .models import *
from Reconinfra_Admin_Panel.models import *

# Create your views here.
def Home(request):
    context = {}
    try:
        form = EnquiryForm()
        all_properties = Properties.objects.all()
        galleyImage = GalleryImages.objects.all()[0:8]
        context['form'] = form
        context['galleyImage'] = galleyImage
        context['all_properties'] = all_properties
    except Exception as e:
        print(e)
    return render(request, 'home/index.html', context)


def ReconinfraAboutUs(request):
    context = {}
    try:
        all_properties = Properties.objects.all()
        context['all_properties'] = all_properties
    except Exception as e:
        print(e)
    return render(request, 'home/about-us.html', context)

def LegalsDocuments(request):
    context = {}
    try:
        all_properties = Properties.objects.all()
        context['all_properties'] = all_properties
    except Exception as e:
        print(e)
    return render(request, 'home/legals-documents.html', context)

def GoldenCityPlotAvailability(request):
    context = {}
    try:
        plot_number = PlotNumber.objects.all()
        all_properties = Properties.objects.all()
        context['plot_number'] = plot_number
        context['all_properties'] = all_properties
    except Exception as e:
        print(e)
    return render(request, 'home/golden-city-plot-availability.html', context)

def GreenValleyPlotAvailability(request):
    context = {}
    try:
        plot_number = PlotNumber.objects.all()
        all_properties = Properties.objects.all()
        context['plot_number'] = plot_number
        context['all_properties'] = all_properties
    except Exception as e:
        print(e)
    return render(request, 'home/green-valley-plot-availability.html', context)


def MissionandVision(request):
    context = {}
    try:
        all_properties = Properties.objects.all()
        context['all_properties'] = all_properties
    except Exception as e:
        print(e)
    return render(request, 'home/mission-and-vision.html', context)


# def CustomerLogin(request):
#     context = {}
#     try:
#         all_properties = Properties.objects.all()
#         context['all_properties'] = all_properties
#     except Exception as e:
#         print(e)
#     return render(request, 'home/login.html', context)

def ReconinfraContactUs(request):
    try:
        context = {}
        if request.method =='POST': 
            form = EnquiryForm(request.POST)
            if form.is_valid():
                form.save()
                name = form.cleaned_data.get('name')
                messages.info(request, "Thank you for getting in touch with Reconinfra! We will get back to you shortly")
                return redirect('/')
            messages.error(request , 'Something went wrong!')
            return redirect("/")
        else:
            form = EnquiryForm()
            context['form'] = form
            all_properties = Properties.objects.all()
            context['all_properties'] = all_properties
    except Exception as e:
        print(e)
    return render(request, 'home/contact-us.html', context)


def PropertiesDetailsView(request, slug):
    context = {}
    try:
        get_details = Properties.objects.get(slug = slug)
        all_properties = Properties.objects.all()
        context['all_properties'] = all_properties
        context['get_details'] = get_details
    except Exception as e:
        print(e)
    return render(request, 'home/property-details.html', context)


def ReconinfraImageGallery(request):
    context = {}
    try:
        galleries = GalleryImages.objects.all()
        all_properties = Properties.objects.all()
        context['all_properties'] = all_properties
        print(galleries)
        context['galleries'] = galleries
    except Exception as e:
        print(e)
    return render(request, 'home/image-gallery.html', context)

def ReconinfraTermsAndConditions(request):
    context = {}
    try:
        all_properties = Properties.objects.all()
        context['all_properties'] = all_properties
    except Exception as e:
        print(e)
    return render(request, 'home/terms-and-conditions.html', context)

def ReconinfraPrivacyPolicy(request):
    context = {}
    try:
        all_properties = Properties.objects.all()
        context['all_properties'] = all_properties
    except Exception as e:
        print(e)
    return render(request, 'home/privacy-policy.html', context)

def ReconinfraDisclaimer(request):
    context = {}
    try:
        all_properties = Properties.objects.all()
        context['all_properties'] = all_properties
    except Exception as e:
        print(e)
    return render(request, 'home/disclaimer.html', context)

def CustomerProfile(request):
    customer = request.session.get('customer_username')
    print(customer)
    if customer is None:
        return redirect('/customer-login/')
    context = {}
    try:
        plot_bookings = PlotBooking.objects.filter(customer_username=customer)
        bookings = PlotBooking.objects.get(customer_username=customer)
        emi_history = EMIHistory.objects.filter(booking_id=bookings.booking_id)
        context['plot_bookings'] = plot_bookings
        context['emi_history'] = emi_history
    except Exception as e:
        print(e)
    return render(request, 'home/customer-profile.html', context)



def EMIHistoryView(request):
    return render(request, "home/emi-history.html")


def CustomerLogin(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['customer_username']
            password = form.cleaned_data['customer_password']
            customer = PlotBooking.objects.filter(customer_username=username).first()
            print(username, password)
            if customer is not None:
                if customer.customer_password == password:
                    request.session['customer_username'] = customer.customer_username
                    return redirect('/customer-profile/')
                else:
                    messages.error(request, "Invalid login credentials")
                    return render(request, 'home/login.html', {'form': form})
            else:
                messages.error(request, "Invalid login credentials")
                return render(request, 'home/login.html', {'form': form})
    else:
        form = CustomerLoginForm()
    return render(request, 'home/login.html', {'form': form})