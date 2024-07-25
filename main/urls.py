from django.urls import path
from main import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('room-page/<int:pk>', views.RoomView.as_view(), name='room'),
    path('create-room/', views.create_room, name='create-room'),
]