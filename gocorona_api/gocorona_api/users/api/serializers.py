from rest_framework import serializers

from gocorona_api.users.models import User, CoronaApp, LANGUAGE_CHOICES, STYLE_CHOICES

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class CoronaAppSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100, default='a')
    status = serializers.IntegerField(default=0)

    latitude= serializers.FloatField(default=0)
    longitude= serializers.FloatField(default=0)
    #required=True, 

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return CoronaApp.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)

        instance.save()

        return instance
