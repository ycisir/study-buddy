from django.shortcuts import render
from main.models import Room
from main.forms import RoomForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


class HomeView(ListView):
	model = Room
	template_name = 'main/home.html'
	context_object_name = 'rooms'

class RoomView(DetailView):
	model = Room
	template_name = 'main/room.html'
	context_object_name = 'room'

def create_room(request):
	context = {}
	return render(request, 'main/room_form.html', context)