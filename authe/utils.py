from django.core.mail import send_mail
from django.conf import settings

def send_register_mail(message, email):
    send_mail('Authe', message, settings.EMAIL_FROM, [email,])