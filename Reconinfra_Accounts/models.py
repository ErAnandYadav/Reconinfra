from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .managers import UserManager
from django.conf import settings
from django.db import models
import string
import random
import uuid


# Create your models here.


class Country(models.Model):
    sortname = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.name

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    username = None
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'),unique=True)
    phone_number = models.CharField(max_length=17, null=True,)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(upload_to='Recon/User/Profile-Picture', null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_facilitator = models.BooleanField(default=False)
    is_accountent = models.BooleanField(default=False)
    aadhar_number = models.CharField(max_length=20, null=True, blank=True)
    aadhar_front = models.ImageField(upload_to='Recon/User/Aadhar', null=True, blank=True)
    aadhar_back = models.ImageField(upload_to='Recon/User/Aadhar', null=True, blank=True)
    pan_number = models.CharField(max_length=11, null=True, blank=True)
    pan_front = models.ImageField(upload_to='Recon/User/PAN', null=True, blank=True)
    pan_back = models.ImageField(upload_to='Recon/User/PAN', null=True, blank=True)
    account_holder_name = models.CharField(max_length = 50, null=True, blank=True)
    account_number= models.CharField(max_length=25, null=True, blank=True)
    ACCOUNT_TYPE = (
        ('Saving', 'Saving'),
        ('Current', 'Current')
    )
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE, default='Saving', null=True, blank=True)
    ifsc_code = models.CharField(max_length=15, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    branch_name = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING, null=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True)
    address = models.CharField(max_length=150, null=True)
    referred_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='children', null=True, blank=True)
    sponsor_id = models.CharField(max_length = 500, null=True, blank=True)
    is_wallet_active = models.BooleanField(default=False)
    BUSINESS_LEVEL = (
        ('Level1', 'Level1'),
        ('Level2', 'Level2'),
        ('Level3', 'Level3'),
        ('Level4', 'Level4'),
        ('Level5', 'Level5'),
        ('Level6', 'Level6'),
        ('Level7', 'Level7'),
        ('Level8', 'Level8'),
        ('Level9', 'Level9'),
        ('Level10', 'Level10'),
    )
    business_level = models.CharField(max_length=20, null=True, blank=True, choices=BUSINESS_LEVEL, default='Level1')
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return f' {self.first_name} {self.last_name} ({self.sponsor_id})'

    def save(self, *args, **kwargs):  # new
        if not self.sponsor_id:
            self.sponsor_id = generator_sponsor_id()
        return super().save(*args, **kwargs)
    
    def calculate_total_business(self):
        # Calculate total business for this team member
        return PlotBooking.objects.filter(associate_id=self.sponsor_id).aggregate(wallet_balance=Sum("down_payment"))['wallet_balance'] or 0

    def get_parent_users(self):
        parent_users = [self]
        current_user = self
        while current_user.referred_by:
            parent = current_user.referred_by
            if parent.business_level >= current_user.business_level:
                parent_users.append(parent)
            current_user = parent
        return parent_users
    

    

    
def generator_sponsor_id(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




class Group(models.Model):
    group_name = models.CharField(max_length=100, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.group_name}'

class GroupInitialize(models.Model):
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True)
    agent = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

