from django.contrib import admin
from .models import Customer, UserInfo, authenticationInfo


# Register your models here.
admin.site.register(Customer)
admin.site.register(UserInfo)
# admin.site.register(authenticationInfo)
