from django import forms
from main.models import Room
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class RoomForm(forms.ModelForm):
	class Meta:
		model = Room
		fields = '__all__'
		exclude = ['host', 'participants']

class LoginForm(AuthenticationForm):
	username = UsernameField()
	password = forms.CharField(widget=forms.PasswordInput())

class SignupForm(UserCreationForm):

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):

	class Meta:
		model = User
		fields = ['username', 'email']