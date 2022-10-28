from django.urls import path

from .views import CreateLink, EditLink

urlpatterns = [
    path('', CreateLink.as_view(), name="create_link"),
    path('<int:pk>', EditLink.as_view(), name="edit_link")
]