from django.urls import path

from .views import CreateLink, EditLink, GetNetworks

urlpatterns = [
    path('', CreateLink.as_view(), name="create_link"),
    path('<int:pk>', EditLink.as_view(), name="edit_link"),
    path('networks', GetNetworks.as_view(), name="get_networks"),
]