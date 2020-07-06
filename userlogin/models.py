from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    is_rf = models.BooleanField(default=False)
    is_eme = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)


class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='setting')
    email_notification = models.BooleanField(default=False)

    def __str__(self):
        return 'user {}'.format(self.user.username)