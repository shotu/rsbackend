from rest_framework import serializers
from .models import Fivep
 
class FivepSerializer(serializers.ModelSerializer):
    # id = serializers.UUIDField()
    class Meta:
        model=Fivep
        fields=('id', 'email', 'phone','dob','app_vendor_login_url',
                'app_name','app_source', 'app_user_id', 'app_password', 'app_user_key','app_encryption_key',
                'app_vendor_key','app_response_callback_url','is_active', 
                'request_token','description',)


class FivepCallbackSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Todo
        fields = ["RequestToken"]