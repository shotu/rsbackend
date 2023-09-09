from django.urls import path

from . import views


urlpatterns = [
    path(
        "emission_templates",
        views.EmissionTemplateListAPIView.as_view(),
        name="emissions_templates",
    ),
    path(
        "emission_templates/<int:id>",
        views.EmissionTemplateListAPIView.as_view(),
        name="emissions_template",
    ),
]
