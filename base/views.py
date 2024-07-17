
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# for flash messages
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Room, Topic
from .forms import RoomForm
# Create your views here.

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        try:
            user=User.objects.get(username=username)
        except:
            # Invalid credentials
            messages.error(request,'User does not exist' )     


        
        if user is not None:
            # Correct credentials
            login(request, user)
            return redirect('home') 
         # Redirect to a success page.
        else:
            messages.error(request,'Username or password is incorrect')
    context={'page':page}
    return render(request, 'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')
    
def registerPage(request):
    page='register'
    return render('base/login_register.html')

    
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

# decorators
@login_required(login_url='login')
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
@login_required(login_url='login')

def updateRoom(request,pk):
    room =Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.user!=room.user:
        return HttpResponse('You are not allowed here!')
    #this condition redirect the user back to home on submission.  
    if request.method=='POST':
        form= RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.user:
        return HttpResponse('You are not allowed here!')

    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':room})