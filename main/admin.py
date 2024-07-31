from django.contrib import admin
from main.models import Room, Topic, Message

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'description', 'updated', 'created']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'room', 'body', 'updated', 'created']