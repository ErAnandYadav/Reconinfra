
from django.db import models

# Create your models here.



class ContactUs(models.Model):
    name = models.CharField(max_length=100, null=True, blank=False)
    phone = models.CharField(max_length=100, null=True, blank=False)
    subject = models.CharField(max_length=100, null=True)
    message = models.TextField(null=True)

    def __str__(self):
        return self.name + ' ' + self.subject