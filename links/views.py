from accounts.models import Profile
from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated

from .models import Links, Networks
from .serailizers import (FullLinkSerializer, LinkSerializer,
                          NetworkSerializer, ProfileSerializer)


class CreateLink(CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = FullLinkSerializer
    queryset = Links.objects.all()

    def perform_create(self, serializer):
        user = get_object_or_404(Profile, id=self.request.user.id)
        serializer.save(user=user)

class EditLink(UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = LinkSerializer
    queryset = Links.objects.all()

class GetNetworks(ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = NetworkSerializer
    queryset = Networks.objects.all()

class ProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    lookup_url_kwarg = 'username'
    lookup_field = 'username'
    queryset = Profile.objects.all()
