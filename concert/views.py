from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from concert.forms import LoginForm, SignUpForm
from concert.models import Concert, ConcertAttending
import requests as req


# Create your views here.

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.filter(username=username).first()
            if user:
                return render(request, "signup.html", {"form": SignUpForm(), "message": "User already exists"})
            else:
                # Create a new user with hashed password
                new_user = User.objects.create(username=username, password=make_password(password))
                # Log in the new user
                login(request, new_user)
                # Redirect to the index page after successful sign up
                return HttpResponseRedirect(reverse("index"))
        except User.DoesNotExist:
            # Render the signup form with an error message if user does not exist
            return render(request, "signup.html", {"form": SignUpForm(), "message": "User does not exist"})
    # Render the signup form for GET requests
    return render(request, "signup.html", {"form": SignUpForm()})


# def signup(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         try:
#             user = User.objects.filter(username=username).first()
#             if user:
#                 return render(request, "signup.html", {"form": SignUpForm, "message": "user already exist"})
#             else:
#                 user = User.objects.create(
#                     username=username, password=make_password(password))
#                 login(request, user)
#                 return HttpResponseRedirect(reverse("index"))
#         except User.DoesNotExist:
#             return render(request, "signup.html", {"form": SignUpForm})
#     return render(request, "signup.html", {"form": SignUpForm})


# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             return render(request, "login.html", {"form": LoginForm(), "message": "Invalid username or password"})
#     return render(request, "login.html", {"form": LoginForm()})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
        except User.DoesNotExist:
            return render(request, "login.html", {"form": LoginForm})
    return render(request, "login.html", {"form": LoginForm})




def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))




def index(request):
    return render(request, "index.html")


# def songs(request):
#     # songs = {"songs":[]}
#     # return render(request, "songs.html", {"songs": [insert list here]})
#     pass

def songs(request):
    dummy_data = [
        {
            "id": 1,
            "title": "duis faucibus accumsan odio curabitur convallis",
            "lyrics": "Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis."
        }
    ]
    return render(request, "songs.html", {"songs": dummy_data})


# def photos(request):
#     # photos = []
#     # return render(request, "photos.html", {"photos": photos})
#     pass
def photos(request):
    dummy_data = [
        {
            "id": 1,
            "pic_url": "http://dummyimage.com/136x100.png/5fa2dd/ffffff",
            "event_country": "United States",
            "event_state": "District of Columbia",
            "event_city": "Washington",
            "event_date": "11/16/2022"
        }
    ]
    return render(request, "photos.html", {"photos": dummy_data})




# @login_required
# def concerts(request):
#     lst_of_concert = []
#     concert_objects = Concert.objects.all()
#     for item in concert_objects:
#         try:
#             status = item.attendee.filter(user=request.user).first().attending
#         except AttributeError:
#             status = "-"
#         lst_of_concert.append({
#             "concert": item,
#             "status": status
#         })
#     return render(request, "concerts.html", {"concerts": lst_of_concert})


def concerts(request):
    if request.user.is_authenticated:
        lst_of_concert = []
        concert_objects = Concert.objects.all()
        for item in concert_objects:
            try:
                status = item.attendee.filter(
                    user=request.user).first().attending
            except:
                status = "-"
            lst_of_concert.append({
                "concert": item,
                "status": status
            })
        return render(request, "concerts.html", {"concerts": lst_of_concert})
    else:
        return HttpResponseRedirect(reverse("login"))



def concert_detail(request, id):
    if request.user.is_authenticated:
        obj = Concert.objects.get(pk=id)
        try:
            status = obj.attendee.filter(user=request.user).first().attending
        except:
            status = "-"
        return render(request, "concert_detail.html", {"concert_details": obj, "status": status, "attending_choices": ConcertAttending.AttendingChoices.choices})
    else:
        return HttpResponseRedirect(reverse("login"))
    pass


def concert_attendee(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            concert_id = request.POST.get("concert_id")
            attendee_status = request.POST.get("attendee_choice")
            concert_attendee_object = ConcertAttending.objects.filter(
                concert_id=concert_id, user=request.user).first()
            if concert_attendee_object:
                concert_attendee_object.attending = attendee_status
                concert_attendee_object.save()
            else:
                ConcertAttending.objects.create(concert_id=concert_id,
                                                user=request.user,
                                                attending=attendee_status)

        return HttpResponseRedirect(reverse("concerts"))
    else:
        return HttpResponseRedirect(reverse("index"))
