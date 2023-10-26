#models.py
from django.db import models
from django.contrib.auth.models import User

class UserAuthenticationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"Authentication Code for {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

