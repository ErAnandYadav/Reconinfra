from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import uuid

def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP

def send_otp(request):
    email=request.GET.get("email")
    print(email)
    o=generateOTP()
    htmlgen = '<p>Your OTP is <strong>o</strong></p>'
    send_mail('OTP request',o,'<your gmail id>',[email], fail_silently=False, html_message=htmlgen)
    return o
    
def send_forget_password_mail(email, token):
    subject = "Your Forget Password Link"
    message = f"Hi, clink on the link to reset your password http://reconinfra.com/accounts/change-password/{token}/"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    return True