import json

from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse

from .models import PerevalAdded, PerevalAreas, PerevalCoords, PerevalImages, UserTourist
from .serializers import AddedSerializer, AreasSerializer, CoordsSerializer, \
    ImagesSerializer, UserTouristSerializer



class UserTouristViewSet(ModelViewSet):
    queryset = UserTourist.objects.all()
    serializer_class = UserTouristSerializer

    def post(self, request):
        serializer = UserTouristSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=200)


class AreasViewSet(ModelViewSet):
    queryset = PerevalAreas.objects.all()
    serializer_class = AreasSerializer


class CoordsViewSet(ModelViewSet):
    queryset = PerevalCoords.objects.all()
    serializer_class = CoordsSerializer

    def post(self, request):
        serializer = CoordsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=200)


class AddedViewSet(ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = AddedSerializer

    def get(self, request):
        read = self.serializer_class(instance=self.queryset, many=True)
        return Response(read.data)

    def submitData(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            return Response({'id': data.id, 'status': 200, 'message': 'Send successfully'})


class ImagesViewSet(ModelViewSet):
    queryset = PerevalImages.objects.all()
    serializer_class = ImagesSerializer

    def get(self, request):
        read = self.serializer_class(instance=self.queryset, many=True)
        return Response(read.data)

    def post(self, request):
        image = self.serializer_class(data=request.data)
        image.save()
        return Response(image.data)


# class AddedUpdate(UpdateAPIView):
#     queryset = PerevalAdded.objects.all().prefetch_related('user', 'areas', 'coords')
#     serializer_class = AddedUpdateSerializer


# class AddedListView(ListAPIView):
#     queryset = PerevalAdded.objects.all()
#     serializer_class = AddedSerializer
#
#     def get_queryset(self):
#         email = self.kwargs['email']
#         return PerevalAdded.objects.filter(user_tourist__email=email)













