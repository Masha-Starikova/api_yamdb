from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Token(models.Model):
    token = models.CharField(max_length=32, null=True, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    confirmation_code = models.CharField(max_length=4, null=False, blank=False, default='----')