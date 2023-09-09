from django.contrib import admin

# Register your models here.

from django.contrib import admin

# Register your models here.
from .models import Fivep


class FivepAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "phone","dob","app_name","app_source","app_user_id","app_password","app_user_key","app_encryption_key","app_vendor_login_url","app_response_callback_url","app_vendor_key","is_active", "request_token","created_at"]

    
admin.site.register(Fivep, FivepAdmin)
