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


    def __str__(self):
        return self.name
