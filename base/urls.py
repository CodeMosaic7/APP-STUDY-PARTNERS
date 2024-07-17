#urls.py file for the app
from django.urls import path
from . import views
# create URLS here.
urlpatterns = [
    path('login/',views.loginPage, name="login"),
    path('logout/',views.logoutUser, name="logout"),
    path('register/',views.registerPage, name="register"),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    # str value is passed to pk[primary key to link to the database]
    # This will accept requests like http://127.0.0.1:8000/room/1/
    path('create-room/',views.createRoom, name="create-room"),
    path('update-room/<str:pk>/',views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/',views.deleteRoom, name="delete-room"),
]