from django import forms
from .models import ContactUs
from Reconinfra_Admin_Panel.models import PlotBooking

class EnquiryForm(forms.ModelForm):
    name = forms.CharField(error_messages = {
                 'required':"Please Enter your Name"
                 })
    class Meta:
        model = ContactUs
        fields = '__all__'

class CustomerLoginForm(forms.ModelForm):
    customer_username = forms.CharField(max_length=30)
    customer_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = PlotBooking
        fields = ['customer_username', 'customer_password']