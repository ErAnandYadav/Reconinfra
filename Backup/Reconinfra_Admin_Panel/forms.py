from pyexpat import model
from .models import *
from django import forms

class AddPropertyForm(forms.ModelForm):
    class Meta:
        model = Properties
        fields = [
            'name', 
            'location', 
            'city', 
            'plot_map', 
            'plot_types', 
            'description',
            'image_1',
            'image_2',
            'image_3',
            'image_4',
        ]

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertiesImage
        fields = ['properties', 'image']

class AddPlotAvailabilityForm(forms.ModelForm):
    class Meta:
        model = PlotNumber
        fields = ['properties', 'plot_status', 'plot_number']


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

class PlotBookingForm(forms.ModelForm):
    class Meta:
        model = PlotBooking
        fields = '__all__'

class ActivateIdForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = '__all__'

class PlotImageForm(forms.ModelForm):
    class Meta:
        model = PropertiesImage
        fields = '__all__'


from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()


