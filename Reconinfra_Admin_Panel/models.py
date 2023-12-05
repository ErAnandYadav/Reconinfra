from django.db import models
from django.utils.text import slugify 
from Reconinfra_Accounts.models import *
from django.contrib.auth.hashers import make_password
import random

# Create your models here.
class Properties(models.Model):
    name = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image_1 = models.ImageField(upload_to='Recon/Properties-img', null=True, blank=True)
    image_2 = models.ImageField(upload_to='Recon/Properties-img', null=True, blank=True)
    image_3 = models.ImageField(upload_to='Recon/Properties-img', null=True, blank=True)
    image_4 = models.ImageField(upload_to='Recon/Properties-img', null=True, blank=True)
    plot_map = models.FileField(upload_to ='Recon/PlotAvailability', null=True, blank=True)
    PLOT_TYPES = (
        ('Residential','Residential'),
        ('Industrial','Industrial'),
        ('Commercial','Commercial'),
    )
    plot_types = models.CharField(max_length=100, choices=PLOT_TYPES, default='Commercial', null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Override Save method
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Properties, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class PlotNumber(models.Model):
    properties = models.ForeignKey(Properties, on_delete=models.CASCADE, null=True)
    PLOT_STATUS = (
        ('Freeze', 'Freeze'),
        ('Available', 'Available'),
        ('Booked', 'Booked'),
        ('Registerd', 'Registerd'),
    )
    plot_status = models.CharField(max_length=100, choices=PLOT_STATUS, default='Available', null=True)
    plot_number = models.CharField(max_length = 100, null=True, blank=True)
    def __str__(self):
        return self.plot_number


class PropertiesImage(models.Model):
    properties = models.ForeignKey(Properties, on_delete=models.CASCADE)
    image = models.FileField(upload_to='Recon/Properties-img', null=True)

    def __str__(self):
        return self.properties.name
        
class GalleryImages(models.Model):
    image = models.FileField(upload_to='Recon/Media-Center', null=True)

class EMIHistory(models.Model):
    booking_id = models.CharField(max_length=100, null=True)
    PAYMENT_METHOD = (
        ('Cheque','Cheque'),
        ('DD','DD'),
        ('Cash','Cash'),
        ('NEFT/IMPS/RTGS','NEFT/IMPS/RTGS'),
    )
    payment_method = models.CharField(max_length=100,choices=PAYMENT_METHOD, default="N/A", null=True)
    number = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2 ,null=True, blank=True)
    payment_date = models.CharField(max_length=100,null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    BOOKING_STATUS = (
        ('Saved', 'Saved'),
        ('Approved', 'Approved'),
        ('Disapproved', 'Disapproved'),
    )
    emi_status = models.CharField(max_length=100, null=True, blank=True)
    booking_status = models.CharField(max_length=100, choices=BOOKING_STATUS, default='Saved', null=True, blank=True)

    def __str__(self):
        return f'{self.booking_id} - {self.amount}'

class PlotBooking(models.Model):
    associate_id = models.CharField(max_length=10, null=True)
    plot = models.ForeignKey(Properties, on_delete=models.CASCADE, null=True)
    plot_number = models.CharField(max_length=10, null=True, unique=True, error_messages={
        'unique': "This plot number has been already booked!"
    })
    plot_size = models.CharField(max_length=100, null=True,blank=True)
    customer_name = models.CharField(max_length=100, null=True)
    sun_of = models.CharField(max_length=100, null=True)
    dob = models.CharField(max_length=100, null=True, blank=True)
    current_address = models.CharField(max_length=100, null=True, blank=True)
    current_pin_code = models.CharField(max_length=100, null=True)
    permanent_address = models.CharField(max_length=100, null=True, blank=True)
    permanent_pin_code = models.CharField(max_length=100, null=True)
    customer_phone = models.CharField(max_length=100, null=True)
    customer_mobile_phone = models.CharField(max_length=100, null=True)
    customer_email = models.CharField(max_length=100, null=True, blank=True)
    customer_username = models.CharField(max_length=100, null=True, blank=True)
    customer_password = models.CharField(max_length=100, null=True, blank=True)
    customer_aadhar = models.CharField(max_length=100, null=True)
    customer_pan = models.CharField(max_length=100, null=True, blank=True)
    BOOKING_METHOD = (
        ('Full Payment','Full Payment'),
        ('EMI','EMI')
    )
    booking_method = models.CharField(max_length=100,choices=BOOKING_METHOD, default="EMI", null=True)
    EMI_PERIOD = (
        ('12', '12 Months'),
        ('24', '24 Months'),
        ('36', '36 Months'),
        ('48', '48 Months'),
        ('60', '60 Months'),
    )
    emi_period = models.CharField(max_length=100,choices=EMI_PERIOD, default=0, null=True, blank=True)
    PAYMENT_METHOD = (
        ('Cheque','Cheque'),
        ('DD','DD'),
        ('Cash','Cash'),
        ('NEFT/IMPS/RTGS','NEFT/IMPS/RTGS'),
    )
    payment_method = models.CharField(max_length=100,choices=PAYMENT_METHOD, default="Cash", null=True)
    cheque_number = models.CharField(max_length=100, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    plot_rate_square_fit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    down_payment = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    remaining_balance = models.DecimalField(max_digits=20, default=0, decimal_places=2, null=True, blank=True)
    BOOKING_STATUS = (
        ('Saved', 'Saved'),
        ('Approved', 'Approved'),
        ('Disapproved', 'Disapproved'),
    )
    booking_status = models.CharField(max_length=100, choices=BOOKING_STATUS, default='Saved', null=True)
    booking_date = models.CharField(max_length=100, null=True)
    EMI_DATE = (
        ('05', '05'),
        ('25', '25'),
    )
    emi_date = models.CharField(max_length=50, choices=EMI_DATE, null=True, blank=True)
    booking_id = models.CharField(max_length=100, null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        if self.down_payment:
            self.remaining_balance = self.total_amount - self.down_payment
        super(PlotBooking, self).save(*args, **kwargs)

    def calculate_emi(self):
        emi = self.emi_period
        if emi is None:
            emi = 0
        remaining_balance = self.remaining_balance
        if remaining_balance is None:
            remaining_balance = 0
        if self.remaining_balance > 0 and int(emi) > 0:
            emi_amount = remaining_balance / int(emi)
            return round(emi_amount, 2)
        else:
            return 0
            
    def set_password(self, raw_password):
        self.customer_password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.customer_password)



class Wallet(models.Model):
    associate = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    business_level = models.CharField(max_length=20, null=True, blank=True)
    plot_number = models.CharField(max_length=100, null=True, blank=True)
    wallet_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    total_business = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.associate}  Your Wallet Balance is  {self.wallet_balance}'


class TransferRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_transfer_requests', null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Reward(models.Model):
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    product_type = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    business = models.IntegerField(null=True, blank=True)
    product_image = models.ImageField(upload_to='Recon/User/Reward', null=True, blank=True)
    is_lock = models.BooleanField(default=False)
    time_limit = models.CharField(max_length=100, null=True,)
    STATUS_CHOICES = (
        ('Lock', 'Lock'),
        ('Unlock', 'Unlock'),
        ('Claimed', 'Claimed'),
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Lock', null=True, blank=True)
    
    def __str__(self):
        return f"{self.product_type} - {self.title}"


class ClaimedReward(models.Model):
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, null=True)
    associate = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    claim_date = models.DateTimeField(auto_now_add=True, null=True)
    STATUS_CHOICES = (
        ('Requested', 'Requested'),
        ('Transferd', 'Transferd'),
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True, blank=True)
    
class PlotAvailabilities(models.Model):
    properties = models.ForeignKey(Properties, on_delete=models.CASCADE, null=True)
    PLOT_STATUS = (
        ('hold', 'Hold'),
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('registered', 'Registered'),
        ('pending', 'Pending'),
    )
    plot_status = models.CharField(max_length=100, choices=PLOT_STATUS, default='available', null=True)
    plot_dimensions = models.CharField(max_length=100, null=True, blank=True)
    plot_number = models.CharField(max_length = 100, null=True, unique=True, blank=True, error_messages ={"unique":"Plot Number Already Exist"})
    def __str__(self):
        return self.plot_number