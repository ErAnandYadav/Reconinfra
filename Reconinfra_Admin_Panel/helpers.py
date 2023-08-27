import random

def pin_generate():
    pin = random.randint(1000, 9999)
    print("this is helpers pin", pin)
    return pin

def generate_booking_id():
    booking_id = random.randint(100000, 999999)
    return booking_id


def assign_label(balance):
    if balance >= 0 and balance <= 1000000:
        return "First Label"
    elif balance >= 1500000:
        return "Second Label"
    else:
        return "No Label"