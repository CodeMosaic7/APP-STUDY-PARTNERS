from django.shortcuts import render
# Create your views here.
rooms=[
    {'id':1, 'name':'Lets learn python!'},
    {'id':2, 'name':'Design with me!'},
    {'id':3, 'name':'Frontend Developers'},
    {'id':4, 'name':'Backend Developers'}
]



def home(request):
    context={'rooms':rooms}
    return render(request,'base/home.html',context)
#now it will the webpage in templates folder in this case 'home.html.
# home has access to each room in rooms list
def room(request, pk):
    room=None
    for i in rooms:
        if i['id']==int(pk):
            room=i
    context={'room':room}
    return render(request,'base/room.html',context)
