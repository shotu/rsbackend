from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from .models import EmissionTemplate
from .permissions import IsOwner
from .serializers import EmissionTemplatesSerializers

# Create your views here.


class EmissionTemplateListAPIView(ListCreateAPIView):
    serializer_class = EmissionTemplatesSerializers

    queryset = EmissionTemplate.objects.all()

    permission_classes = [permissions.IsAuthenticated, IsOwner]

    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
