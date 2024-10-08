from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('rooms/', views.GetRooms.as_view()),
    path('rooms/<int:pk>', views.GetRoom.as_view()),
]