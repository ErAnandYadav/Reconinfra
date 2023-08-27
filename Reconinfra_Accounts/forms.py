from django import forms
from .models import CustomUser,Group,GroupInitialize
from django.forms import ModelForm, ValidationError

class UserRegisterForm(forms.ModelForm):
    class Meta:
      model = CustomUser
      fields = [
        'first_name', 
        'last_name',
        'email',
        'phone_number',
        'aadhar_number',
        'pan_number',
        'account_holder_name',
        'account_number',
        'account_type',
        'ifsc_code',
        'bank_name',
        'branch_name',
        'country',
        'state',
        'city',
        'address',
        'sponsor_id',
        'password'
      ]
class UpdateRegisterForm(forms.ModelForm):
    class Meta:
      model = CustomUser
      fields = [
        'first_name', 
        'last_name',
        'email',
        'phone_number',
        'aadhar_number',
        'pan_number',
        'account_holder_name',
        'account_number',
        'account_type',
        'ifsc_code',
        'bank_name',
        'branch_name',
        'country',
        'state',
        'city',
        'address',
      
      ]
    
class UserUpdateForm(forms.ModelForm):
  class Meta:
      model = CustomUser
      fields = [
        'profile_pic',
        'first_name', 
        'last_name',
        'email',
        'phone_number',
        'aadhar_number',
        #'aadhar_front',
        #'aadhar_back',
        'pan_number',
        #'pan_front',
        #'pan_back',
        # 'account_holder_name',
        # 'account_number',
        # 'account_type',
        # 'ifsc_code',
        # 'bank_name',
        # 'branch_name',
        # 'country',
        'state',
        'city',
        'address',  
      ]
class UpdateBankDetailsForm(forms.ModelForm):
  class Meta:
    model = CustomUser
    fields = [
        'account_holder_name',
        'account_number',
        'account_type',
        'ifsc_code',
        'bank_name',
        'branch_name',
      ]

class GroupForm(forms.ModelForm):
  class Meta:
    model = Group
    fields = ['group_name']

class GroupInitializeForm(forms.ModelForm):
  class Meta:
    model = GroupInitialize
    fields = ['group','agent','is_admin']