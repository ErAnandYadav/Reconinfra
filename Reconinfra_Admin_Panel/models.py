from django.db import models
from django.utils.text import slugify 
from Reconinfra_Accounts.models import *

# Create your models here.
class Properties(models.Model):
    name = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    plot_map = models.FileField(upload_to = 'Recon/PlotAvailability', null=True, blank=True)
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
    properties = models.ForeignKey(Properties, on_delete=models.DO_NOTHING)
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

import random
class PlotBooking(models.Model):
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True)
    plot = models.ForeignKey(Properties, on_delete=models.CASCADE, null=True)
    booking_id = models.CharField(max_length=6, null=True, blank=True)
    plot_availability = models.ForeignKey(PlotNumber, on_delete=models.CASCADE, null=True)
    pin = models.CharField(max_length=100, null=True, blank=True)
    customer_name = models.CharField(max_length=100, null=True)
    customer_father_name = models.CharField(max_length=100, null=True)
    customer_phone = models.CharField(max_length=100, null=True)
    plot_number = models.CharField(max_length=100, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    down_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    PAYMENT_METHOD = (
        ('Full Payment','Full Payment'),
        ('EMI','EMI')
    )
    payment_method = models.CharField(max_length=100,choices=PAYMENT_METHOD, default="EMI", null=True)
    EMI_PERIOD = (
        ('12', '12 Months'),
        ('18', '18 Months')
    )
    emi_period = models.CharField(max_length=100,choices=EMI_PERIOD, default="12 Months", null=True)
    STATUS_CHOICES = (
        ('Approved','Approved'),
        ('Pending','Pending'),
        ('Rejected','Rejected')
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending", null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        # return self.plot.name + ' - ' + self.customer_name
        return f'{self.plot.name}    Plot No. {self.plot_number}   Booking ID {self.booking_id}'


class PaymentHistory(models.Model):
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    booking = models.ForeignKey(PlotBooking, on_delete=models.DO_NOTHING, blank=True)
    pin = models.CharField(max_length=100, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pay_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    PAYMENT_METHOD = (
        ('Full Payment','Full Payment'),
        ('EMI','EMI')
    )
    payment_method = models.CharField(max_length=100,choices=PAYMENT_METHOD, default="EMI", null=True)
    EMI_PERIOD = (
        ('12', '12 Months'),
        ('18', '18 Months')
    )
    emi_period = models.CharField(max_length=100,choices=EMI_PERIOD, default="12 Months", null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.agent}'

    class Meta:
        ordering = ['-created_at']

class Wallet(models.Model):
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    balance = models.IntegerField(default = 0)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.agent}  Your Wallet Balance is  {self.balance}'


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
    product_image = models.ImageField(upload_to='Recon/User/Reward', null=True, blank=True)
    is_lock = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_type} - {self.title}"
