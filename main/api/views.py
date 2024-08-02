from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from main.models import Room
from .serializers import RoomSerializer

def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return JsonResponse(routes, safe=False)

class GetRooms(GenericAPIView, ListModelMixin):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class GetRoom(GenericAPIView, RetrieveModelMixin):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)