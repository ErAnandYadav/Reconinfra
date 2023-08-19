from dataclasses import fields
from pyexpat import model
from .models import *
from django import forms

class AddPropertyForm(forms.ModelForm):
    class Meta:
        model = Properties
        fields = ['name', 'location', 'city', 'plot_map', 'plot_types', 'description']


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertiesImage
        fields = ['properties', 'image']

class AddPlotAvailabilityForm(forms.ModelForm):
    class Meta:
        model = PlotNumber
        fields = ['properties', 'plot_status', 'plot_number']


class PlotBookingForm(forms.ModelForm):
    class Meta:
        model = PlotBooking
        fields = [
            'location','plot',
            'plot_availability',
            'customer_name',
            'customer_father_name',
            'customer_phone',
            'plot_number',
            'total_amount',
            'down_payment',
            'payment_method',
            'emi_period',
        ]

class PaymentHistoryForm(forms.ModelForm):
    class Meta:
        model = PaymentHistory
        fields = ['agent','booking','total_amount','pay_payment','payment_method','emi_period']


class AddGalleryImagesForm(forms.ModelForm):
    class Meta:
        model = GalleryImages
        fields = ['image']

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['product_type','title','description','product_image']                                           
                                          

class TransferRequestForm(forms.ModelForm):
    class Meta:
        model = TransferRequest
        fields = ['amount']

class WithdrawalsRequestForm(forms.ModelForm):
    class Meta:
        model = TransferRequest
        fields = '__all__'