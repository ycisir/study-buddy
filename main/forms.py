from django import forms
from main.models import Room, User
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, UserChangeForm, EmailMultiAlternatives

class RoomForm(forms.ModelForm):
	class Meta:
		model = Room
		fields = '__all__'
		exclude = ['host', 'participants']

class SignupForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['name', 'username', 'email', 'password1', 'password2']

class UserUpdateForm(UserChangeForm):
	password = None
	class Meta:
		model = User
		fields = ['avatar', 'name' ,'username', 'email', 'bio']
