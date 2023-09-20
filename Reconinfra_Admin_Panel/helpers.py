from django.core.mail import EmailMessage
from django.conf import settings
import random
import string
import time

def pin_generate():
    pin = random.randint(1000, 9999)
    print("this is helpers pin", pin)
    return pin

def generate_booking_id():
    random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
    timestamp = int(time.strftime("%Y")[2:])
    booking_id = f'RG{timestamp:02d}{random_string}'
    return booking_id

def send_email(html_content, subject, email):
    subject = 'Booking Confirmation'
    message = html_content
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    email = EmailMessage(subject, message, email_from, recipient_list)
    try:
        email.send()
    except Exception as e:
        print(e)

def send_email2(html_content, subject, email):
    subject = 'Booking Confirmation'
    message = html_content
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    email = EmailMessage(subject, message, email_from, recipient_list)
    try:
        email.send()
    except Exception as e:
        print(e)

# Commission calculate
def calculate_commission(pay_payment, business_level):
    commission_rates = {
        'Level1': 5,
        'Level2': 7,
        'Level3': 8,
        'Level4': 9,
        'Level5': 10,
        'Level6': 11,
        'Level7': 12,
        'Level8': 13,
        'Level9': 14,
        'Level10': 15,
    }
    commission_rate = commission_rates.get(business_level, 0)
    return pay_payment * commission_rate / 100


COMMISSION_SLABS = [
    (1000000, "Level1"),
    (3000000, "Level2"),
    (6000000, "Level3"),
    (15000000, "Level4"),
    (30000000, "Level5"),
    (60000000, "Level6"),
    (100000000, "Level7"),
    (150000000, "Level8"),
    (250000000, "Level9"),
    (400000000, "Level10"),
]

def find_commission_level(total_amount):
    for slab, level in COMMISSION_SLABS:
        if total_amount <= slab:
            return level
    return None  # If total_amount is greater than the highest slab



from datetime import datetime, timedelta



emi = round(10000 / 12,2)
current_date = datetime.now()
payment_dates = []

for _ in range(12):
    next_month = current_date + timedelta(days=30)  # Assuming a 30-day month
    payment_date = next_month.replace(day=5)
    if payment_date < next_month:
        payment_date += timedelta(days=30)
    payment_dates.append(payment_date.strftime("%Y-%m-%d"))
    current_date = next_month

# Create a list of dictionaries containing date and EMI for each month
emi_list = [{'date': date, 'emi': emi} for date in payment_dates]