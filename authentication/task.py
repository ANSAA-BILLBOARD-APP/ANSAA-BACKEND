import threading, random, string
from django.utils import timezone
from django.conf import settings
from . models import OTP
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from twilio.http.async_http_client import AsyncTwilioHttpClient
from twilio.rest import Client


class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        self.email_message.reply_to = ['noreply@ansaa.com']
        self.email_message.from_email = 'Ansaa <noreply@example.com>'
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


def generate_otp():
        # Generate a 4-digit OTP
        otp = ''.join(random.choices(string.digits, k=4))
        return otp

def send_otp_email(email, otp_code):
    # Send OTP email
    email_subject = 'Ansaa OTP'
    template = loader.get_template('mail_template.txt')
    parameters = {'otp': otp_code}
    email_content = template.render(parameters)

    email_message = EmailMultiAlternatives(
        email_subject,
        email_content,
        settings.EMAIL_HOST_USER,
        [email]
    )
    email_message.content_subtype = 'html'
    EmailThread(email_message).start()

    
def send_otp_sms(phone_number, otp_code):
    account_sid = 'ACf70ef8fd878f32665058f3b67e6b67c6'
    auth_token = '360d3291e72f2f13594cfe473c4d67c8'
    client = Client(account_sid, auth_token)
    verification_check = client.verify
    message = client.messages.create(
                            from_='+12512379462',
                            body= f"Your [ANSAA] verification code is: {otp_code}. Don't share this code with anyone; Ansaa will never ask for the code.",
                            to=phone_number
                        )

    print(message.sid)



    


