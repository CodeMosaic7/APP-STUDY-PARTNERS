from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm
# Create your views here.

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(Q(topic__name__icontains=q)| Q(name__icontains=q) | Q(description__icontains=q))
    #chatgpt it
    topics=Topic.objects.all()
    room_count=rooms.count()
    context={'rooms':rooms, 'topics':topics,'room_count':room_count}
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

# View to edit room properties
def updateRoom(request,pk):
    room =Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    #this condition redirect the user back to home on submission.  
    if request.method=='POST':
        form= RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request, 'base/room_form.html',context)

def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':room})