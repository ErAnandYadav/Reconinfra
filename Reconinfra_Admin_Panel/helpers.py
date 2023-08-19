import random

def pin_generate():
    pin = random.randint(1000, 9999)
    print("this is helpers pin", pin)
    return pin

def generate_booking_id():
    booking_id = random.randint(100000, 999999)
    return booking_id


