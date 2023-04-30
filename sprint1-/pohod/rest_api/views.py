import json

from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse

from .models import PerevalAdded, PerevalAreas, PerevalCoords, PerevalImages
from .serializers import AddedSerializer, AreasSerializer, CoordsSerializer, \
    ImagesSerializer, AddedUpdateSerializer
from .services import PerevalData


class AreasViewSet(ModelViewSet):
    queryset = PerevalAreas.objects.all()
    serializer_class = AreasSerializer


class CoordsViewSet(ModelViewSet):
    queryset = PerevalCoords.objects.all()
    serializer_class = CoordsSerializer


class AddedViewSet(ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = AddedSerializer


class ImagesViewSet(ModelViewSet):
    queryset = PerevalImages.objects.all()
    serializer_class = ImagesSerializer


class AddedUpdate(UpdateAPIView):
    queryset = PerevalAdded.objects.all().prefetch_related('user', 'areas', 'coords')
    serializer_class = AddedUpdateSerializer


class AddedListView(ListAPIView):
    queryset = PerevalAdded.objects.all()
    serializer_class = AddedSerializer

    def get_queryset(self):
        email = self.kwargs['email']
        return PerevalAdded.objects.filter(user_tourist__email=email)


def submit_data(request):
    if request.method == 'POST':
        data_control = PerevalData(request.body)
        if data_control.check_data():
            data_control.submit_data()
        result = data_control.format_result()
    elif request.method == 'GET':
        if 'user__email' in request.GET:
            data_control = PerevalData(request.body)
            result = data_control.get_email(request.GET.get('user__email'))
        else:
            result = {'result': f'not found'}
    else:
        result = {'result': f'not {request.method} support'}

    return HttpResponse(json.dumps(result))

def send_data(request, *args, **kwargs):
    pass










