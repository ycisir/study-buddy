from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from main.models import Room, Topic
from main.forms import RoomForm, LoginForm, SignupForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db.models import Q
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(ListView):
	model = Room
	template_name = 'main/home.html'
	context_object_name = 'rooms'


	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
		rooms = Room.objects.filter(
			Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(desc__icontains=q)
		)

		room_count = rooms.count()
		topics = Topic.objects.all()
		context['rooms'] = rooms
		context['topics'] = topics
		context['q'] = q
		context['room_count'] = room_count
		return context


class RoomView(DetailView):
	model = Room
	template_name = 'main/room.html'
	context_object_name = 'room'

	def get_context_data(self, **kwargs):
		context = super(RoomView, self).get_context_data(**kwargs)
		room_messages = context['room'].message_set.all().order_by('-created')
		context['room_messages'] = room_messages
		return context




@method_decorator(login_required(login_url='login'), name='dispatch')
class CreateRoom(CreateView):
	form_class = RoomForm
	template_name = 'main/room_form.html'
	success_url = '/'

	def get_context_data(self, **kwargs):
		context = super(CreateRoom, self).get_context_data(**kwargs)
		context['page'] = 'create'
		return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateRoom(UpdateView):
	model = Room
	form_class = RoomForm
	template_name = 'main/room_form.html'
	success_url = '/'
	

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteRoom(DeleteView):
	model = Room
	success_url = '/'
	template_name = 'main/confirm_delete.html'

class UserLogin(LoginView):
	template_name = 'main/register_login.html'
	authentication_form = LoginForm
	success_url = 'home'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		return super().dispatch(request, *args, **kwargs)

class UserLogout(LogoutView):
    next_page = '/'

class UserSignup(FormView):
	form_class = SignupForm
	template_name = 'main/register_login.html'

	def get_context_data(self, **kwargs):
		context = super(UserSignup, self).get_context_data(**kwargs)
		context['page'] = 'register'
		return context

	def form_valid(self, form):
		user = form.save(commit=False)
		user.username = user.username.lower()
		user.save()
		return redirect('login')

	