from django.db import models

import uuid
# from django.utils.translation import ugettext_lazy as _


class Fivep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    phone = models.IntegerField(unique=True)#  unique=True)
    email = models.EmailField(unique=True)  
    dob = models.CharField(max_length=255) # intentionally kept as Charfield
    app_name = models.CharField(max_length=255)
    app_source = models.CharField(max_length=255)
    app_user_id = models.CharField(max_length=255)
    app_password = models.CharField(max_length=255)
    app_user_key = models.CharField(max_length=255)
    app_encryption_key = models.CharField(max_length=255)
    app_vendor_login_url = models.CharField(max_length=255)
    app_vendor_key = models.CharField(max_length=255)
    app_response_callback_url =  models.CharField(max_length=255)
    request_token = models.CharField(max_length=255)
    
    access_token = models.CharField(max_length=255,default='your_default_value')
    jwt_token = models.CharField(max_length=255,null=True, blank=True)
    
    
    client_code = models.CharField(max_length=255,null=True, blank=True)
    
    
    is_deleted = models.BooleanField(default=False)  # for soft delete
    is_active = models.BooleanField(default=True)  # Set to
    updated_at = models.DateTimeField(auto_now=True)  # when updated
    created_at = models.DateTimeField(auto_now_add=True)  # when created
    created_by  = models.CharField(max_length=255, default="SYSTEM")
    description = models.TextField(max_length=255)
    
        