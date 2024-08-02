from django.urls import path
from main import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('room/<int:pk>', views.RoomView.as_view(), name='room'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='user-profile'),
    path('topics/', views.TopicsPage.as_view(), name='topics'),
    path('activity/', views.ActivityPage.as_view(), name='activity'),


    path('create/', views.CreateRoom.as_view(), name='create'),
    path('update/<int:pk>', views.UpdateRoom.as_view(), name='update'),
    path('delete/<int:pk>', views.DeleteRoom.as_view(), name='delete'),
    path('delete-message/<int:pk>', views.DeleteMessage.as_view(), name='delete-message'),
    path('update-user/<int:pk>', views.UpdateUser.as_view(), name='update-user'),

    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('signup/', views.UserSignup.as_view(), name='signup'),
    
]