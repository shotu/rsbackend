from rest_framework import serializers

from .models import EmissionTemplate


class EmissionTemplatesSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmissionTemplate
        fields = ["title", "id", "image_url", "description", "status"]
