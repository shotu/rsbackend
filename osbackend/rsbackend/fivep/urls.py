from django.urls import path

from . import views
# urls.py in your app
from django.urls import path
from .views import CustomAPIView


# urlpatterns = [
#     path('/fivep',views.getFiveptoken),
#     path('post/',views.postFiveptoken),
# ]
# refer=https://docs.djangoproject.com/en/4.2/topics/http/urls/

action_dict = {
        'get': 'list',
        'post': 'create',
        'get': 'retrieve',
        # 'put': 'update',
        # 'patch': 'partial_update',
        # 'delete': 'destroy',
    }
 
urlpatterns = [
    path(
        "fivep",
        views.FivepListAPIView.as_view(),
        name="fivep",
    ),
    path(
        "fivep/<uuid:id>",
        views.FivepDetailAPIView.as_view(),
        name="fivep",
    ),
    # path('callback/', views.Five5CallbackAPIView.as_view(action_dict)),
    path('callback/<uuid:id>', CustomAPIView.as_view(), name='custom-api'),
]
