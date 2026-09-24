from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from news.models import News
from .forms import RegisterUserForm, LoginForm


def index(request):
    news = News.objects.filter(
        status="approved"
    ).order_by("-data")[:3]

    return render(request, "main/index.html", {"news": news})

def about(request):
    return render(request, "main/about.html")


def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save()

            users_group = Group.objects.get(name="Users")
            user.groups.add(users_group)

            auth_login(request, user)

            return redirect("index")
    else:
        form = RegisterUserForm()

    return render(request, "main/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            auth_login(request, form.user)
            return redirect("index")
    else:
        form = LoginForm()

    return render(request, "main/login.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect("index")
