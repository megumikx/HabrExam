from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from news.models import News


def index(request):
    news = News.objects.order_by('-data')[:3]
    return render(request, 'main/index.html', {'news': news})


def about(request):
    return render(request, "main/about.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()

    return render(request, "main/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("index")
    else:
        form = AuthenticationForm()

    return render(request, "main/login.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect("index")