from django.db import models
from django.conf import settings
from .resource import ModeratorStatus



class UserTourist(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=50)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=155, blank=True)
    last_name = models.CharField(max_length=155, blank=True)


class PerevalAreas(models.Model):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey(to='self', name='parent', null=True, on_delete=models.SET_NULL)


class PerevalCoords(models.Model):
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    height = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.latitude} {self.longitude} {self.height}'


class PerevalAdded(models.Model):
    user_tourist = models.ForeignKey(UserTourist, null=True, on_delete=models.SET_NULL)
    pereval_areas = models.ForeignKey(PerevalAreas, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now=True)
    add_time = models.DateTimeField(auto_now=True)

    beauty_title = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    other_titles = models.CharField(max_length=100, blank=True, null=True)
    connect = models.CharField(max_length=100, blank=True, null=True)
    coords = models.ForeignKey(PerevalCoords, on_delete=models.CASCADE, blank=True, null=True)

    winter = models.CharField(max_length=50, verbose_name='Зима', blank=True, null=True)
    summer = models.CharField(max_length=50, verbose_name='Лето', blank=True, null=True)
    autumn = models.CharField(max_length=50, verbose_name='Осень', blank=True, null=True)
    spring = models.CharField(max_length=50, verbose_name='Весна', blank=True, null=True)

    status = models.SmallIntegerField(default=ModeratorStatus.new, choices=ModeratorStatus.choices)

    @property
    def is_new(self):
        return self.status == ModeratorStatus.new

    def __str__(self):
        return f'{self.title} {self.status}'

    def set_level(self, **kwargs):
        self.winter = kwargs.get('winter', '')
        self.summer = kwargs.get('summer', '')
        self.autumn = kwargs.get('autumn', '')
        self.spring = kwargs.get('spring', '')
        self.save()

    def get_level(self):
        dic_level = {}
        dic_level['winter'] = self.winter
        dic_level['summer'] = self.summer
        dic_level['autumn'] = self.autumn
        dic_level['spring'] = self.spring
        return dic_level


class PerevalImages(models.Model):
    data_img = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE, related_name='image', blank=True, null=True)
    image = models.ImageField(upload_to='images', blank=True)
    title = models.CharField(max_length=100, blank=True, null=True)


class SprActivitiesTypes(models.Model):
    title = models.CharField(max_length=255)




