import random

from django.core.mail import send_mail
from django.db.models import Q
from django.utils.crypto import get_random_string

from reviews.models import Token, User


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
        confirmation_code=str(random.randint(1000, 9999))
        new_token_obj = Token(
            user=new_user,
            confirmation_code=confirmation_code
        )
        new_token_obj.save()
        send_confirmation_code(confirmation_code, email)
        return True
    return False


def update_token(username, confirmation_code):
    token = None
    user = User.objects.get(username=username)
    token_obj = Token.objects.get(user=user)
    if token_obj.confirmation_code == confirmation_code:
        token = get_random_string(length=32)
        token_obj.token = token
        token_obj.save()
    return token