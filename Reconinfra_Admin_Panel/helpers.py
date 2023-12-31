from django.core.mail import EmailMessage
from datetime import datetime, timedelta
from django.conf import settings
from Reconinfra_Admin_Panel.models import EMIHistory, PlotBooking
from django.db.models import Sum
from django.db.models import Q
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




def convert_into_emi(amount, booking_id, months):
    amount = float(amount)
    months = int(months)
    emi = round(amount / months, 2)
    current_date = datetime.now()
    payment_dates = []

    for _ in range(months):
        next_month = current_date + timedelta(days=30)
        while next_month.day != 5:
            next_month += timedelta(days=1)
        payment_dates.append(next_month.strftime("%Y-%m-%d"))
        current_date = next_month
    emi_list = [{'emi_date': date, 'emi_amount': emi, 'booking_id': booking_id} for date in payment_dates]
    EMIHistory.objects.bulk_create([EMIHistory(**emi_data) for emi_data in emi_list])

    print(emi_list)

# Example usage:
# amount = 10000
# booking_id = 12345
# months = 12
# convert_into_emi(amount, booking_id, months)


def amount_human_format(amount):
    final_amount = amount
    print(final_amount,"4555555555555")
    if final_amount is None:
        return 0.00
    amount = float('{:.3g}'.format(amount))
    magnitude = 0
    while abs(amount) >= 1000:
        magnitude += 1
        amount /= 1000.0
    return '{}{}'.format('{:f}'.format(amount).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])



def filter_monthely_balance():
    current_date = datetime.now()
    # two_days_in_future = current_date + timedelta(days=0)
    # print(two_days_in_future)
    start_date = datetime(current_date.year, current_date.month, 1)

    # Calculate the end date (1st of the next month)
    end_date = start_date + timedelta(days=32)
    end_date = datetime(end_date.year, end_date.month, 1)

    # Build the query to filter records between start_date and end_date
    query = Q(created_at__gte=start_date, created_at__lt=end_date)
    print(query,"578787")
    # Fetch records that match the query
    balance = PlotBooking.objects.filter(query).aggregate(total_balance=Sum('down_payment'))['total_balance']
    return balance


