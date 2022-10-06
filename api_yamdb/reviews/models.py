from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user')
    )
    role = models.CharField(max_length=20, choices=ROLES, default='user')
