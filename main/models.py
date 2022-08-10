from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='is activated?')
    send_message = models.BooleanField(default=True, verbose_name='Are you need notification about new comments?')

    class Meta(AbstractUser.Meta):
        pass

# Create your models here.
