from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.user.username

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    age = models.BigIntegerField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    orders = models.BigIntegerField()
    VIP_STATES_CHOICES = [
        ('platinum', 'Platinum'),
        ('gold', 'Gold'),
    ]
    vip_status = models.CharField(max_length=50, choices=VIP_STATES_CHOICES)
    created_by = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', default='default_profile_image.jpg')



    def __str__(self):
        return self.name


class logHistory(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=False, null=False)
    previous_value = models.CharField(max_length=255, blank=False, null=False)
    new_value = models.CharField(max_length=255, blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


# store authentication information in hashed_password and hashed_username fields
class authenticationInfo(models.Model):
    username = models.CharField(max_length=255, blank=False, null=False)
    adminPassword = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.username
