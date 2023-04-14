from django.urls import path
from rest_framework import routers

from .views import AreasViewSet, CoordsViewSet, AddedViewSet, ImagesViewSet, AddedListView


router = routers.DefaultRouter()
router.register('areas', AreasViewSet)
router.register('coords', CoordsViewSet)
router.register('added', AddedViewSet)
router.register('images', ImagesViewSet)

urlpatterns = [
    path('added_list/<email>', AddedListView.as_view())
]
















