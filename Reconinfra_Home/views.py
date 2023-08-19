from queue import PriorityQueue
from django.contrib import messages
from django.shortcuts import render, HttpResponse,redirect
from .forms import EnquiryForm
from .models import *
from Reconinfra_Admin_Panel.models import *

# Create your views here.
def Home(request):
    context = {}
    try:
        form = EnquiryForm()
        all_properties = Properties.objects.all()
        galleyImage = GalleryImages.objects.all()
        context['form'] = form
        context['galleyImage'] = galleyImage
        context['all_properties'] = all_properties
    except Exception as e:
        print(e)
    return render(request, 'home/index.html', context)


def ReconinfraAboutUs(request):
    return render(request, 'home/about-us.html')

def LegalsDocuments(request):
    return render(request, 'home/legals-documents.html')

def PlotAvailability(request):
    plot_number = PlotNumber.objects.all()
    return render(request, 'home/plot-availability.html', {'plot_number' : plot_number})


def MissionandVision(request):
    return render(request, 'home/mission-and-vision.html')


def CustomerLogin(request):
    return render(request, 'home/login.html')

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
    except Exception as e:
        print(e)
    return render(request, 'home/contact-us.html', context)


def PropertiesDetailsView(request, slug):
    context = {}
    try:
        get_details = Properties.objects.get(slug = slug)
        context['get_details'] = get_details
    except Exception as e:
        print(e)
    return render(request, 'home/property-details.html', context)


def ReconinfraImageGallery(request):
    context = {}
    try:
        galleries = GalleryImages.objects.all()
        print(galleries)
        context['galleries'] = galleries
    except Exception as e:
        print(e)
    return render(request, 'home/image-gallery.html', context)

def ReconinfraTermsAndConditions(request):
    return render(request, 'home/terms-and-conditions.html')

def ReconinfraPrivacyPolicy(request):
    return render(request, 'home/privacy-policy.html')

def ReconinfraDisclaimer(request):
    return render(request, 'home/disclaimer.html')

def CustomerProfile(request):
    return render(request, 'home/customer-profile.html')



