from django.urls import path
from rest_framework import routers

from .views import AreasViewSet, CoordsViewSet, AddedViewSet, ImagesViewSet


router = routers.DefaultRouter()
router.register('areas', AreasViewSet)
router.register('coords', CoordsViewSet)
router.register('added', AddedViewSet)
router.register('images', ImagesViewSet)


PerevalAdded = AddedViewSet.as_view({
    'post': 'create'
})
PerevalAdded_detail = AddedViewSet.as_view({
    'get': 'retrieve',
    'patch': 'update',
})
PerevalAdded_list = AddedViewSet.as_view({
    'get': 'list'
})

urlpatterns = [
    # path('added_list/', AddedListView.as_view()),
    # path('submitData/', AddedViewSet.as_view({'post': 'submitData'})),
    path('submitData/', PerevalAdded, name='PerevalAdded'),
    path('submitData/<int:pk>', PerevalAdded_detail, name='PerevalAdded_detail'),
    path('submitData/', PerevalAdded_list, name='PerevalAdded_list'),
]
















