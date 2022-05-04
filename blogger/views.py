from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from . import models
from .models import Background, Follow, Notice, User, Message, Cikes, Mlikes, Comment, Collect


def index(request):
    if request.user.is_authenticated:
        f = models.Follow.objects.filter(fans=request.user).values_list('following', flat=True)
        msgs = models.Message.objects.select_related('user', 'o_ID').filter(Q(user__in=f, show=True) | Q(user=request.user))
        return render(request, "index.html", {
            'msgs': msgs,
            "bg": get_colors(request.user)
        })
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
            user.profilePhoto = picture
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
    msg = Message(user=request.user)
    msg.content = request.POST["content"]
    h = request.POST["h"]
    msg.pic = request.FILES.get("picture")
    # 公开
    if h == "n":
        msg.show = True
    # 粉丝可见
    else:
        msg.show = False
    msg.save()
    return HttpResponseRedirect(reverse("index"))


def showuser(request, u_id):
    user = models.User.objects.get(username=u_id)
    ctx = {'user': user, 'bg': get_colors(u_id)}
    if request.method == "GET":
        if request.user == user:
            ctx['flag'] = False
            msgs = models.Message.objects.filter(user=u_id).select_related('o_ID')
            ctx['msgs'] = msgs
        else:
            msgs = models.Message.objects.filter(user=u_id, show=True).select_related('o_ID')
            ctx['msgs'] = msgs
            ctx['flag'] = True
            fol = models.Follow.objects.filter(following=user, fans=request.user)
            if fol:
                ctx['btn_class'] = "btn btn-success"
            else:
                ctx['btn_class'] = "btn btn-default"
        return render(request, "user.html", ctx)
    else:
        if request.POST['h'] == "fol":
            following = User.objects.get(username=u_id)
            fan = request.user
            fol = Follow.objects.filter(following=following, fans=fan)
            n = Notice.objects.get(user=following)
            if fol:
                fol.first().delete()
                n.save()
            else:
                Follow(following=following, fans=fan).save()
                n.fans += 1
                n.save()
        else:
            inf = request.POST["change_inf"]
            user.introduction = inf
            user.save()
        return HttpResponseRedirect("/user/" + u_id)


def clike(request, m_id):
    m = Comment.objects.get(ID=m_id)
    user = request.user
    n = Notice.objects.get(user=m.user)
    c = Cikes.objects.filter(comment_id=m, user=user)
    if c:
        a = c.first()
        a.delete()
    else:
        Cikes.objects.create(comment_id=m, user=user)
        n.likes += 1
    n.save()
    return HttpResponseRedirect(reverse("index"))


def createcomment(request, m_id):
    m = Message.objects.get(ID=m_id)
    user = request.user
    comment = request.POST["content"]
    Comment.objects.create(message_id=m, user=user, content=comment)
    n = Notice.objects.get(user=m.user)
    n.comments += 1
    n.save()
    return HttpResponseRedirect("/bloginf/" + m_id)


def mlike(request, m_id):
    m = Message.objects.get(ID=m_id)
    user = request.user
    n = Notice.objects.filter(user=m.user)
    ml = Mlikes.objects.filter(message_id=m, user=user)
    if ml:
        a = ml.first()
        a.delete()
    else:
        Mlikes.objects.create(message_id=m, user=user)
        n.likes += 1
    n.save()
    return HttpResponseRedirect(reverse("index"))


def collect(request, m_id):
    m = Message.objects.get(ID=m_id)
    user = request.user
    if Collect.objects.filter(message_id=m, user=user):
        a = Collect.objects.get(message_id=m, user=user)
        a.delete()
    else:
        Collect.objects.create(message_id=m, user=user)
    return HttpResponseRedirect(reverse("index"))


def relay(request, m_id):
    m = Message.objects.get(ID=m_id)
    content = request.POST["content"]
    content = content + "//@" + m.user.username + ":" + m.content
    user = request.user
    Message.objects.create(user=user, content=content, o_ID=m.o_ID)
    n = Notice.objects.get(user=m.user)
    n.relays += 1
    n.save()
    return HttpResponseRedirect(reverse("index"))


def bloginf(request, m_id):
    msg = models.Message.objects.select_related('user').filter(ID=m_id)
    cms = models.Comment.objects.select_related('user').filter(message_id=m_id)
    return render(request, "bloginf.html", {
        "msgs": msg,
        "cms": cms,
        'bg': get_colors(msg.first().user.username)
    })


def mlike1(request, m_id):
    m = Message.objects.get(ID=m_id)
    user = request.user
    ml = Mlikes.objects.filter(message_id=m, user=user)
    n = Notice.objects.get(user=m.user)
    if ml:
        a = ml.first()
        a.delete()
    else:
        Mlikes.objects.create(message_id=m, user=user)
        n.likes += 1
    n.save()
    return HttpResponseRedirect("/bloginf/" + m_id)


def listlike(request):
    mlike = Mlikes.objects.select_related('user').select_related('message_id')
    clike = Cikes.objects.select_related('user').select_related('comment_id')
    return render(request, "listl.html", {"mlikes": mlike, "clikes": clike, 'bg': get_colors(request.user)})


def listcollect(request):
    collect = Collect.objects.select_related('user')
    return render(request, "listl.html", {"mlikes": collect, 'bg': get_colors(request.user)})


def listcomment(request):
    comments = Comment.objects.select_related('user').select_related('message_id')
    return render(request, "listl.html", {"coms": comments, 'bg': get_colors(request.user)})


def listfollow(request):
    f = Follow.objects.filter(fans=request.user).select_related('following')
    return render(request, "listfollow.html", {"fs": f, "content": "关注", 'bg': get_colors(request.user),
                                               'flag': True})


def listfan(request):
    f = Follow.objects.filter(following=request.user).select_related('fans')
    return render(request, "listfollow.html", {"fs": f, "content": "粉丝", 'bg': get_colors(request.user,),
                                               'flag': False})


def changeuser(request):
    user = request.user
    email = request.POST["email"]
    pic = request.FILES.get("pic")
    user.email = email
    user.profilePhoto = pic
    user.save()
    return HttpResponseRedirect("cu")


def cu(request):
    user = request.user
    return render(request, "changeuser.html", {"user": user, 'bg': get_colors(request.user)})


def notice(request):
    user = request.user
    n = Notice.objects.get(user=user)
    likes = n.likes
    relays = n.relays
    comments = n.comments
    fans = n.fans
    n.likes = 0
    n.relays = 0
    n.comments = 0
    n.fans = 0
    n.save()
    return render(request, "notice.html", {"likes": likes, "relays": relays, "comments": comments, "fans": fans,
                                           'bg': get_colors(request.user)})


def search(request):
    text = request.POST["text"]
    ms = Message.objects.all()
    m = [i for i in ms if text in i.content]
    us = User.objects.all()
    u = [i for i in us if text in i.username]
    return render(request, "result.html", {"msgs": m, "us": u, 'bg': get_colors(request.user)})


def color(request):
    c = request.GET['color']
    user = request.user
    bg = Background.objects.get(user=user)
    if c == "green":
        bg.back_color = "#b4d64e"
        bg.font_color = "#000000"
        bg.box_color = "#FFFFFF"
        bg.link_color = "#da7a30"
    elif c == "yellow":
        bg.back_color = "#dac6a1"
        bg.font_color = "#000000"
        bg.box_color = "#FFFFFF"
        bg.link_color = "#217dae"
    elif c == "darkred":
        bg.back_color = "#6d1b27"
        bg.font_color = "#af9296"
        bg.box_color = "#210406"
        bg.link_color = "#b9404f"
    else:
        bg.back_color = "#FFFFFF"
        bg.font_color = "#000000"
        bg.box_color = "#FFFFFF"
        bg.link_color = "#3079ed"
    bg.save()
    return HttpResponseRedirect(reverse("index"))


def get_colors(u_id):
    bg = Background.objects.get(user=u_id)
    return bg
