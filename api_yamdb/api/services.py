import random

from django.core.mail import send_mail
from django.db.models import Q
from django.utils.crypto import get_random_string
from reviews.models import User


def send_confirmation_code(code, recipient):
    send_mail(
        subject='Confirmation code',
        message=f'Your confirmation code: {code}',
        from_email='yamdb@mail.com',
        recipient_list=[recipient],
        fail_silently=False
    )


def create_user(username, email):
    if not User.objects.filter(Q(username=username) | Q(email=email)).exists():
        new_user = User(username=username, email=email)
        new_user.set_password(User.objects.make_random_password(length=10))
        new_user.save()
        confirmation_code = str(random.randint(1000, 9999))
        send_confirmation_code(confirmation_code, email)
        return True
    return False
