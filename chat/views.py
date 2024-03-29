from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def index(request):
    return render(request, "chat/index.html")


@login_required(login_url='/login/')
def room(request, room_name):
    username = request.user
    return render(request, "chat/room.html", {"room_name": room_name,
                                              "username": username})
