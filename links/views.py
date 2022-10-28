from accounts.models import Profile
from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView,
                                     UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Links, Networks
from .serailizers import LinkSerializer, NetworkSerializer


class CreateLink(CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = LinkSerializer
    queryset = Links.objects.all()

    def perform_create(self, serializer):
        user = get_object_or_404(Profile, id=self.request.user.id)
        serializer.save(user=user)

class EditLink(UpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = LinkSerializer
    queryset = Links.objects.all()
