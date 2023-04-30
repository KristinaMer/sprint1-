from .models import *
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField



class UserTouristSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, allow_blank=False)
    phone = serializers.CharField(allow_blank=True)
    username = serializers.CharField(allow_blank=True)
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)

    def ceate(self, validated_data):
        return UserTourist.objects.create(**validated_data)



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

    def create(self, validated_fata):
        return PerevalCoords.objects.create(**validated_fata)


class ImagesSerializer(serializers.ModelSerializer):
    # pereval_added = serializers.PrimaryKeyRelatedField(queryset=PerevalAdded.objects.all())
    image = Base64ImageField()

    class Meta:
        model = PerevalImages
        fields = ['id', 'image', 'pereval_added', 'title']

    def create(self, validated_data):
        image = validated_data.pop('image')
        pereval_added = validated_data('pereval_added')
        title = validated_data('title')
        return PerevalImages.objects.create(image=image, pereval_added=pereval_added, title=title)


class AddedSerializer(serializers.ModelSerializer):
    user_tourist = serializers.PrimaryKeyRelatedField(queryset=UserTourist.objects.all())
    pereval_areas = serializers.PrimaryKeyRelatedField(queryset=PerevalAreas.objects.all())
    coords = serializers.PrimaryKeyRelatedField(queryset=PerevalCoords.objects.all())

    class Meta:
        model = PerevalAdded
        fields = [
            'id',
            'user_tourist',
            'pereval_areas',
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

    def create(self, validated_data, **kwargs):
        user_instance = validated_data.pop('user')
        coords_instance = validated_data.pop('coords')
        image_instance = validated_data.pop('image')

        user = UserTourist.objects.create(**user_instance)
        coords = PerevalCoords.objects.create(**coords_instance)
        added = PerevalAdded.objects.create(**validated_data, user=user, coords=coords, status='new')

        for image in image_instance:
            img = image.pop('image')
            title = image.pop('title')
            PerevalImages.objects.create(image=img, added=added, title=title)

        return added


# class AddedUpdateSerializer(serializers.ModelSerializer):
#     user_tourist = serializers.PrimaryKeyRelatedField(queryset=UserTourist.objects.all())
#     pereval_areas = serializers.PrimaryKeyRelatedField(queryset=PerevalAreas.objects.all())
#     coords = serializers.PrimaryKeyRelatedField(queryset=PerevalCoords.objects.all())
#
#     def validate(self, attrs):
#         if not self.instance.is_new:
#             raise serializers.ValidationError({'status': ['---']})
#         return super().validate(attrs)
#
#     class Meta:
#         model = PerevalAdded
#         fields = [
#             'id',
#             'user_tourist',
#             'pereval_areas',
#             'date_added',
#             'add_time',
#             'beauty_title',
#             'other_titles',
#             'title',
#             'connect',
#             'coords',
#             'winter',
#             'summer',
#             'autumn',
#             'spring',
#             'status',
#         ]























