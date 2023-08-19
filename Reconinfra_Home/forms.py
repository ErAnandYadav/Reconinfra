from django import forms
from .models import ContactUs


class EnquiryForm(forms.ModelForm):
    name = forms.CharField(error_messages = {
                 'required':"Please Enter your Name"
                 })
    class Meta:
        model = ContactUs
        fields = '__all__'