from django.contrib import admin
from .models import Customer, UserInfo,logHistory
from django.db import models
from django.utils.html import format_html


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address', 'age', 'phone_number', 'orders', 'vip_status', 'created_by', 'profile_image_preview')
    list_filter = ('vip_status', 'created_by')
    search_fields = ('name', 'email', 'phone_number', 'address')
    readonly_fields = ('profile_image_preview',)


    def profile_image_preview(self, obj):
        from django.utils.html import format_html
        if obj.profile_image:

            return format_html('<img src="{}" style="width: 45px; height:45px;" />', obj.profile_image.url)
        return "-"
    profile_image_preview.short_description = "Profile Image"


class LogTableAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description', 'previous_value', 'new_value', 'created_time', 'profile_image_preview')
    readonly_fields = ('profile_image_preview',)

    def profile_image_preview(self, obj):
        if obj.user:
            customers = Customer.objects.filter(created_by=obj.user).order_by('-id')  # Example: ordering by the newest
            if customers.exists():
                # Just use the first customer's image or specify any other logic you prefer
                return format_html('<img src="{}" style="width: 45px; height:45px;" />', customers.first().profile_image.url)
        return "-"
    profile_image_preview.short_description = "Profile Image"

# admin.site.register(LogTable, LogTableAdmin)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(UserInfo)
admin.site.register(logHistory, LogTableAdmin)
