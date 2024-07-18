
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# for flash messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Room, Topic, Message
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
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
           user=form.save(commit=False)
           user.username=user.username.lower()
           user.save()
           login(request,user)
           return redirect('home')

        else:
           messages.error(request,'Error occured during registration')
    return render(request, 'base/login_register.html',{'form':form})

    
def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(Q(topic__name__icontains=q)| Q(name__icontains=q) | Q(description__icontains=q))
    #chatgpt it
    topics=Topic.objects.all()
    room_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms, 'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

#now it will the webpage in templates folder in this case 'home.html.
# home has access to each room in rooms list
def room(request, pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    # will sort the messages in recent order
    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)

@login_required(login_url='login')
def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    # to get all children
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)
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

@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user!=message.user:
        return HttpResponse('You are not allowed here!')

    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':message})

