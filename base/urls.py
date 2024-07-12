#urls.py file for the app
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    # str value is passed to pk[primary key to link to the database]
    # This will accept requests like http://127.0.0.1:8000/room/1/

]