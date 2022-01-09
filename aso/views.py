from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

from django.contrib.auth import authenticate, login, logout
from .forms import OrderForm, CreateUserForm
from .models import Room, Message

from django.contrib.auth.decorators import login_required

from django.contrib import messages


@login_required(login_url='login')
def index(request):
    context = {}
    return render(request, 'templates/home.html', context)


@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'templates/home.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect("login")

        context = {'form': form}
        return render(request, 'templates/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, "templates/login.html", context)


@login_required(login_url='login')
def room(request, room):
    username = request.GET.get('username')
    roomDetails = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': roomDetails,
    })


@login_required(login_url='login')
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/' + room + '/?username=' + username)
    else:
        newRoom = Room.objects.create(name=room)
        newRoom.save()
        return redirect('/' + room + '/?username=' + username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    newMessage = Message.objects.create(
        value=message, user=username, room=room_id
    )
    newMessage.save()
    return HttpResponse()


def getMessages(request, room):
    roomDetails = Room.objects.get(name=room)
    messages = Message.objects.filter(room=roomDetails.id)
    return JsonResponse({
        'messages': list(messages.values())
    })
