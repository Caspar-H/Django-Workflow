from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    is_rf = models.BooleanField(default=False)
    is_eme = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

