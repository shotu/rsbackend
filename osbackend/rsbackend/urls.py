"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Onescope  API",
        default_version="v1",
        description="Onescope APIs ",
        terms_of_service="https://www.onescope.ai/policies/terms/",
        contact=openapi.Contact(email="contact@os.local"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# router = DefaultRouter()
# router.register(r"mvp", views.render) TODO add here mvp


urlpatterns = [
    # path("admin/", admin.site.urls),
    path("admin/", admin.site.urls),
    # path("auth/", include("rsbackend.authentication.urls")),
    # path("mvp/", include("rsbackend.mvp.urls")),
    path("fivep/", include("rsbackend.fivep.urls")),
    # path(
    #     "social_auth/",
    #     include(("social_auth.urls", "social_auth"), namespace="social_auth"),
    # ),
    # path("mvp/", include("mvp.urls")),
    # path("income/", include("income.urls")),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path(
        "api/api.json/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
