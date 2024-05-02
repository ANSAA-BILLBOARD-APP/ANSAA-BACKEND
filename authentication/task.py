import threading, random, string
from django.utils import timezone
from . models import OTP
from django.core.mail import EmailMultiAlternatives


class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        self.email_message.reply_to = ['noreply@ansaa.com']
        email_message.from_email = 'Ansaa <noreply@example.com>'
        threading.Thread.__init__(self)


    def run(self):
        self.email_message.send()

def generate_otp():
        # Generate a 6-digit OTP
        otp = ''.join(random.choices(string.digits, k=6))
        # expiration_time = timezone.now() + timezone.timedelta(minutes=5)
        # # Save OTP to database
        # otp_instance = OTP.objects.create(email=email, otp=otp, expiration_time=expiration_time)
        return otp
    


