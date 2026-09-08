from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from .models import Event


def home(request):
    events = Event.objects.all()
    return render(request, "home.html", {"events": events})


def event(request):
    if request.method == "POST":
        title = request.POST.get("title")
        date = request.POST.get("date")
        time = request.POST.get("time")
        location = request.POST.get("location")
        description = request.POST.get("description")

        Event.objects.create(
            title=title,
            date=date,
            time=time,
            location=location,
            description=description
        )

        return redirect("/events/")

    return render(request, "event.html")


def events(request):
    events = Event.objects.all()
    return render(request, "events.html", {"events": events})


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def register(request):
    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "registration.html", {
                "error": "Passwords do not match."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "registration.html", {
                "error": "Username already exists."
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name
        )

        return redirect("/login/")

    return render(request, "registration.html")


def login(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("/")

        return render(request, "login.html", {
            "error": "Invalid username or password."
        })

    return render(request, "login.html")