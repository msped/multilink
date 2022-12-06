from accounts.models import Profile
from rest_framework import serializers

from .models import Links, Networks

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Networks
        fields = [
            'id',
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
            'id',
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
    profile_picture = serializers.ImageField()
    
    class Meta:
        model = Profile
        fields = [
            'id',
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
