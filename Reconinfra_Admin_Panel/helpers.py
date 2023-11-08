from django.core.mail import EmailMessage
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Sum
from django.db.models import Q
from django.http import JsonResponse
from decimal import Decimal
from Reconinfra_Accounts.models import *
from .models import *
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
def calculate_commission(paid_amount, business_level):
    print(paid_amount, business_level,"544545")
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
    return paid_amount * commission_rate / 100


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
    emi_hostory = EMIHistory.objects.filter(booking_id=booking_id).first()
    for _ in range(months):
        next_month = current_date + timedelta(days=30)
        while next_month.day != 5:
            next_month += timedelta(days=1)
        payment_dates.append(next_month.strftime("%Y-%m-%d"))
        current_date = next_month
    emi_list = [{'payment_date': date, 'amount': emi, 'booking_id': booking_id} for date in payment_dates]
    print('emi_list:',emi_list)
    # if emi_hostory:
    #     for x in emi_list:
    #         emi = EMIHistory(
    #             amount= x['amount'],
    #             payment_date= x['payment_date'],
    #             booking_id=x['booking_id']
    #         )
    #         emi.save()
    EMIHistory.objects.bulk_create([EMIHistory(**emi_data) for emi_data in emi_list])


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





def commission_distribution(amount, sponsor_id):
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
    sponsor_id = sponsor_id
    initial_total_commission = 15
    print("initial_total_commission",initial_total_commission)
    user = CustomUser.objects.get(sponsor_id=sponsor_id)
    user.is_wallet_active = True
    my_business_level = user.business_level
    my_commission_percentage = commission_rates.get(my_business_level, 0)
    my_commission_amount = amount * my_commission_percentage/100
    agent_wallet, created = Wallet.objects.get_or_create(associate_id=user.account_id)
    agent_wallet.wallet_balance += Decimal(my_commission_amount)
    agent_wallet.total_business += Decimal(my_commission_amount)
    agent_wallet.is_active = True
    agent_wallet.save()
    
    initial_total_commission = initial_total_commission - my_commission_percentage
    
    parent_users = user.get_parent_users()
    higher_business_users = [parent for parent in parent_users if my_business_level < parent.business_level]
    
    percentage_list = []
    for x in higher_business_users:
        users = CustomUser.objects.get(account_id=x.account_id)
        parents_percentage = commission_rates.get(users.business_level, 0)
        percentage_list.append(parents_percentage)
    print("Percentage list:-",percentage_list)
    
    differences = [percentage_list[i] - percentage_list[i - 1] for i in range(1, len(percentage_list))]
    differences = [percentage_list[0] - my_commission_percentage] + differences
    print("Differences:-",differences)
    
    distributed_commission = 0
    commissions = []

    for difference in differences:
        if distributed_commission + difference <= initial_total_commission:
            commission = (amount * difference) / 100
            commissions.append(round(commission, 2))
            distributed_commission += difference
        else:
            # Calculate the remaining commission to reach 15%
            remaining_commission = initial_total_commission - distributed_commission
            commission = (amount * remaining_commission) / 100
            commissions.append(round(commission, 2))
            distributed_commission += remaining_commission
            break
    
    for i, x in enumerate(higher_business_users):
        if i < len(commissions):
            user = CustomUser.objects.get(account_id=x.account_id)
            
            agent_wallet, created = Wallet.objects.get_or_create(associate_id=user.account_id)
            agent_wallet.wallet_balance += Decimal(commissions[i])
            agent_wallet.total_business += Decimal(commissions[i])
            agent_wallet.is_active = True
            agent_wallet.save()

            user.is_wallet_active = True
            user.save()
            
            print(f"Saved {commissions[i]} commission to {user.first_name}'s wallet.")
        else:
            print(f"Commission data not available for user {x.email}")
    data = ({
        "Higher Business User Level": [parent.business_level for parent in higher_business_users],
        "percentage_list": percentage_list,
        "differences": differences,
        "distributed_commission": distributed_commission + my_commission_percentage,
        "remaining_commission": initial_total_commission - distributed_commission,
    })
    return data




from django.db.models import Count
def get_multilevel_chain_count(user):
    count = 0

    # Get the users referred by the current user
    child_users = CustomUser.objects.filter(referred_by=user)

    for child_user in child_users:
        count += 1  # Count the immediate child user
        count += get_multilevel_chain_count(child_user)  # Recursively count their children

    return count


def get_team_business(user):
    total_business = 0

    # Get the child users of the current user
    child_users = CustomUser.objects.filter(referred_by=user)
    
    # Calculate the total business for child users
    child_users_business = PlotBooking.objects.filter(associate_id__in=child_users.values_list('sponsor_id', flat=True))
    total_business += child_users_business.aggregate(total=Sum('down_payment'))['total'] or 0

    # Iterate through child users and sum their team's business
    for child_user in child_users:
        total_business += get_team_business(child_user)  # Recursively sum their team's business

    return total_business