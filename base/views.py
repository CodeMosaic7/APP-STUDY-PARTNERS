from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm
# Create your views here.

def home(request):
    rooms=Room.objects.all()
    context={'rooms':rooms}
    return render(request,'base/home.html',context)
#now it will the webpage in templates folder in this case 'home.html.
# home has access to each room in rooms list
def room(request, pk):
    room=Room.objects.get(id=pk)
   
    context={'room':room}
    return render(request,'base/room.html',context)

def createRoom(request):
    form= RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        # if values are valid save in the database.
    context={'form':form}
    return render(request, 'base/room_form.html',context)
