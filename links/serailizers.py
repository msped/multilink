from accounts.serializers import ProfileSerializer
from rest_framework import serializers

from .models import Links, Networks

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Networks
        fields = [
            'logo',
            'name'
        ]

class LinkSerializer(serializers.ModelSerializer):
    network = serializers.PrimaryKeyRelatedField(
        queryset=Networks.objects.all()
    )

    class Meta:
        model = Links
        fields = [
            'network',
            'link',
            'nsfw'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["network"] = NetworkSerializer(instance.network).data
        return data
