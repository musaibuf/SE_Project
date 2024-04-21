import pywhatkit
import random
import datetime

def generate_otp(length=6):
    """Generate a numeric OTP of specified length."""
    return random.randint(10**(length-1), (10**length)-1)

def send_otp_whatsapp(phone, otp):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute + 1  # Ensure this provides enough time for WhatsApp to load and send the message
    if minute >= 60:  # If minute + 1 results in 60, adjust the hour and reset minute
        minute = 0
        hour = hour + 1 if hour < 23 else 0
    message = f"Your OTP is: {otp}"
    pywhatkit.sendwhatmsg(phone, message, hour, minute, wait_time=20)

def verify_otp(input_otp, actual_otp):
    """Verify that the provided OTP matches the expected OTP."""
    return input_otp == actual_otp
