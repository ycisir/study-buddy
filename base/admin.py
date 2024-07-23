from django.contrib import admin
from base.models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'desc', 'updated', 'created']
