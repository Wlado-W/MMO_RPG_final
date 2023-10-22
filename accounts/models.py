from django.db import models
from django.contrib.auth.models import User


class UsersAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.SmallIntegerField(default=0)
