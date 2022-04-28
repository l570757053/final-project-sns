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
        msgs = models.Message.objects.select_related('user').filter(show=True)
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
            notice = models.Notice(user=user)
            background = models.Background(user=user)
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
    # 公开
    if h == "n":
        show = True
    # 粉丝可见
    else:
        show = False
    msg = models.Message(user=request.user, content=content, show=show, pic=picture)
    msg.save()
    return HttpResponseRedirect(reverse("index"))


def showuser(request, u_id):
    if request.method == "GET":
        user = models.User.objects.get(username=u_id)
        ctx = {'c_style': "col-sm-offset-3", 'user': user}
        if request.user == user:
            ctx['flag'] = False
            msgs = models.Message.objects.filter(user=u_id)
            ctx['msgs'] = msgs
        else:
            msgs = models.Message.objects.filter(user=u_id, show=True)
            ctx['msgs'] = msgs
            ctx['flag'] = True
            fol = models.Follow.objects.filter(following=user, fans=request.user)
            if fol:
                ctx['btn_class'] = "btn btn-success"
            else:
                ctx['btn_class'] = "btn btn-default"
        return render(request, "user.html", ctx)
    else:
        # TODO: 需要填充关注和修改签名，h的值为fol是关注，cha则是修改
        return HttpResponseRedirect("/user/"+u_id)
