from .models import *
from rest_framework import serializers



class UserTouristSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, allow_blank=False)
    phone = serializers.CharField(allow_blank=True)
    username = serializers.CharField(allow_blank=True)
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)


class AreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalAreas
        fields = [
            'id',
            'title',
            'parent',
        ]


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalAreas
        fields = [
            'id',
            'latitude',
            'longitude',
            'height',
        ]


class AddedSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserTourist.objects.all())
    areas = serializers.PrimaryKeyRelatedField(queryset=PerevalAreas.objects.all())
    coords = serializers.PrimaryKeyRelatedField(queryset=PerevalCoords.objects.all())

    class Meta:
        model = PerevalAdded
        fields = [
            'id',
            'user',
            'areas',
            'date_added',
            'add_time',
            'beauty_title',
            'other_titles',
            'title',
            'connect',
            'coords',
            'winter',
            'summer',
            'autumn',
            'spring',
            'status',
        ]


class AddedUpdateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserTourist.objects.all())
    areas = serializers.PrimaryKeyRelatedField(queryset=PerevalAreas.objects.all())
    coords = serializers.PrimaryKeyRelatedField(queryset=PerevalCoords.objects.all())

    def validate(self, attrs):
        if not self.instance.is_new:
            raise serializers.ValidationError({'status': ['---']})
        return super().validate(attrs)

    class Meta:
        model = PerevalAdded
        fields = [
            'id',
            'user',
            'areas',
            'date_added',
            'add_time',
            'beauty_title',
            'other_titles',
            'title',
            'connect',
            'coords',
            'winter',
            'summer',
            'autumn',
            'spring',
            'status',
        ]


class ImagesSerializer(serializers.ModelSerializer):
    pereval_added = serializers.PrimaryKeyRelatedField(queryset=PerevalAdded.objects.all())

    class Meta:
        model = PerevalImages
        fields = ['id', 'image', 'pereval_added']




















