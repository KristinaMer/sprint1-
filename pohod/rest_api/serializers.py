from django.forms import model_to_dict
from rest_framework.exceptions import NotFound
from django.db.utils import OperationalError
from django.core.exceptions import ValidationError

from .models import *
from .utils import DatabaseException, ObjectException
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
        fields = ['id', 'image', 'data_img', 'title']

    def create(self, validated_data):
        image = validated_data.pop('image')
        data_img = validated_data.pop('data_img')
        title = validated_data.pop('title')
        return PerevalImages.objects.create(image=image, data_img=data_img, title=title)


class AddedSerializer(serializers.ModelSerializer):
    user_tourist = serializers.PrimaryKeyRelatedField(queryset=UserTourist.objects.all())
    pereval_areas = serializers.PrimaryKeyRelatedField(queryset=PerevalAreas.objects.all())
    coords = serializers.PrimaryKeyRelatedField(queryset=PerevalCoords.objects.all())
    image = ImagesSerializer(many=True)
    level = serializers.DictField(source='get_level')

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
            'image',
            # 'winter',
            # 'summer',
            # 'autumn',
            # 'spring',
            'level',
            'status',
        ]

    def create(self, validated_data, **kwargs):
        user_instance = validated_data.pop('user_tourist')
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


    def validate(self, data):
        image = data['image']
        for img in image:
            if img['image'] is None:
                raise ValidationError('Image error')

        return data


    def list(self, email):
        result = []
        select_tourist = UserTourist.objects.filter(email=email)
        if select_tourist.exists():
            select_pereval = PerevalAdded.objects.filter(tourist=select_tourist[0])
            for pereval in select_pereval:
                result.append(self.create(pereval.id).decode())

        return result


    def retrieve(self, request):
        pk = request.pop('id')
        try:
            if not PerevalAdded.objects.filter(id=pk).exists():
                raise NotFound
            return super().retrieve(request)
        except OperationalError:
            raise DatabaseException()


    # def update(self, instance, validate_data, **kwargs):
    #     instance.user_instance = validate_data.get('user_tourist', instance.user_instance)
    #     instance.coords_instance = validate_data.get('coords', instance.coords_instance)
    #     instance.image_instance = validate_data.get('image', instance.image_instance)
    #     instance.save()
    #     return instance


    def update(self, request, instance, **kwargs):
        pk = request.id
        user = instance.pop('user', None)
        coords = instance.pop('coords', None)
        image = instance.pop('image', None)
        level = instance.pop('level', None)
        try:
            query = PerevalAdded.objects.filter(id=pk)
            obj = query.first()
            if obj.status != ModeratorStatus.new:
                raise ObjectException
            if coords:
                coords_object = model_to_dict(request.coords)
                coords_object = {**coords_object, **coords}
                coords_object.pop('id', None)
                coords_instance, created = PerevalCoords.objects.get_or_create(**coords_object)
                request.coords = coords_instance
            if level:
                level_object = request.get_level()
                level_object = {**level_object, **level}
                request.set_level(**level_object)
            if image:
                PerevalImages.objects.filter(added=request).delete()

                for img in image:
                    pic = img.pop('image')
                    title = img.pop('title')
                    PerevalImages.objects.create(image=pic, added=request, title=title)

            return super().update(request, instance)
        except OperationalError:
            raise DatabaseException()


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























