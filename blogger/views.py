from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from . import models
from .models import User


def index(request):
    if request.user.is_authenticated:
        f = models.Follow.objects.filter(fans=request.user).values_list('following', flat=True)
        msgs = models.Message.objects.select_related('user').filter(Q(user__in=f) | Q(user=request.user))
    else:
        msgs = models.Message.objects.select_related('user').all()
    return render(request, "index.html", {
        'msgs': msgs
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        picture = request.FILES.get("picture")

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.ProfilePhoto = picture
            notice = models.Notice(user=request.user)
            background = models.Background(user=request.user)
            user.save()
            notice.save()
            background.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


def publish(request):
    content = request.POST["content"]
    h = request.POST["h"]
    picture = request.FILES.get("picture")
    if h == "n":
        show = True
    else:
        show = False
    msg = models.Message(user=request.user, content=content, show=show, pic=picture)
    msg.save()
    return HttpResponseRedirect(reverse("index"))


def showuser(request, u_id):
    user = request.user
    msgs = models.Message.objects.filter(user=u_id)
    return render(request, "user.html", {
        'user': user,
        'msgs': msgs,
        'c_style': "col-sm-offset-3"
    })
