from accounts.models import Profile
from rest_framework import serializers

from .models import Links, Networks

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Networks
        fields = [
            'logo',
            'name'
        ]

class FullLinkSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Links
        fields = [
            'user',
            'network',
            'link',
            'nsfw'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["network"] = NetworkSerializer(instance.network).data
        return data

class LinkSerializer(serializers.ModelSerializer):
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

class ProfileSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'username',
            'first_name',
            'last_name',
            'bio',
            'profile_picture',
            'links',
        ]

    def get_links(self, obj):
        links = Links.objects.filter(user=obj.id)
        serializer = LinkSerializer(links, many=True)
        return serializer.data
