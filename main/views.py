from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from main.models import Room, Topic, Message
from main.forms import RoomForm, LoginForm, SignupForm, UserUpdateForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db.models import Q
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views.generic import TemplateView

class HomeView(ListView):
	model = Room
	template_name = 'main/home.html'
	context_object_name = 'rooms'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
		rooms = Room.objects.filter(
			Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
		)
		room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

		room_count = rooms.count()
		topics = Topic.objects.all()[0:5]
		context['rooms'] = rooms
		context['topics'] = topics
		context['q'] = q
		context['room_count'] = room_count
		context['room_messages'] = room_messages
		return context

class RoomView(DetailView):
	model = Room
	template_name = 'main/room.html'

	def post(self, request, *args, **kwargs):
		room = self.get_object()
		message = Message.objects.create(
			user = request.user,
			room = room,
			body = request.POST.get('body')
		)
		room.participants.add(request.user)
		return redirect('room', pk=room.id)

	def get_context_data(self, **kwargs):
		context = super(RoomView, self).get_context_data(**kwargs)
		room_messages = context['room'].message_set.all().order_by('-created')
		participants = context['room'].participants.all()
		context['room_messages'] = room_messages
		context['participants'] = participants
		return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteMessage(DeleteView):
	model = Message
	success_url = '/'
	template_name = 'main/confirm_delete.html'

	def get_context_data(self, **kwargs):
		context = super(DeleteMessage, self).get_context_data(**kwargs)
		context['page'] = 'message_delete'
		return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class CreateRoom(CreateView):
	form_class = RoomForm
	template_name = 'main/room_form.html'

	def post(self, request, *args, **kwargs):
		topic_name = request.POST.get('topic')
		topic, created = Topic.objects.get_or_create(name=topic_name)
		room = Room.objects.create(
			host= request.user, 
			topic= topic, 
			name= request.POST.get('name'),
			description= request.POST.get('description'),
		)
		return redirect('home')

	def get_context_data(self, **kwargs):
		context = super(CreateRoom, self).get_context_data(**kwargs)
		context['page'] = 'create'
		context['topics'] = Topic.objects.all()
		return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateRoom(UpdateView):
	model = Room
	form_class = RoomForm
	template_name = 'main/room_form.html'

	def post(self, request, *args, **kwargs):
		room = self.get_object()
		topic_name = request.POST.get('topic')
		topic, created = Topic.objects.get_or_create(name=topic_name)
		room.name = request.POST.get('name')
		room.topic = topic
		room.description = request.POST.get('description')
		room.save()
		return redirect('home')

	def get_context_data(self, **kwargs):
		context = super(UpdateRoom, self).get_context_data(**kwargs)
		context['topics'] = Topic.objects.all()
		return context

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


class ProfileView(DetailView):
	model = User
	template_name = 'main/profile.html'

	def get_context_data(self, **kwargs):
		user = self.get_object()
		context = super(ProfileView, self).get_context_data(**kwargs)
		rooms = user.room_set.all()
		room_messages = user.message_set.all()
		topics = Topic.objects.all()
		context['rooms'] = rooms
		context['room_messages'] = room_messages
		context['topics'] = topics
		return context
	

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateUser(UpdateView):
	model = User
	form_class = UserUpdateForm
	template_name = 'main/update_user.html'
	
	def form_valid(self, form):
		user = self.get_object()
		form.save()
		return redirect('user-profile', pk=user.id)


class TopicsPage(TemplateView):
	template_name = 'main/topics.html'

	def get_context_data(self, **kwargs):
		context = super(TopicsPage, self).get_context_data(**kwargs)
		q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
		context['topics'] = Topic.objects.filter(name__icontains=q)
		return context


class ActivityPage(TemplateView):
	template_name = 'main/activity.html'

	def get_context_data(self, **kwargs):
		context = super(ActivityPage, self).get_context_data(**kwargs)
		context['room_messages'] = Message.objects.all()
		return context