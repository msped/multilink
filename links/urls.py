from django.urls import path

from .views import CreateLink

urlpatterns = [
    path('', CreateLink.as_view(), name="create_link"),
]