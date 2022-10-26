from accounts.models import Profile
from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from .models import Links, Networks
from .serailizers import LinkSerializer, NetworkSerializer


class CreateLink(CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = LinkSerializer
    queryset = Links.objects.all()

    def perform_create(self, serializer):
        user = get_object_or_404(Profile, id=self.request.user.id)
        serializer.save(user=user)
